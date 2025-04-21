import csv
import logging
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

from piersfan.config import Config
from piersfan.converter import Converter

Description = """
フィッシングピアースサイトから釣果情報を取得する
"""

_logger = logging.getLogger(__name__)


class Extractor:
    def __init__(self):
        """
        初期化
        :param homepage_url: 横浜フィッシングピアーズホームページURL
        """

    def get_javascript_url(self, homepage_url: str) -> str:
        """
        ホームページから <script type="module"> タグの src 属性を抽出し、
        JavaScript ファイルの URL を返します。
        """
        res = requests.get(homepage_url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        script_tag = soup.find("script", {"type": "module", "src": True})
        js_path = script_tag["src"] if script_tag else None

        if not js_path:
            raise RuntimeError("JavaScriptファイルが見つかりませんでした。")

        return urljoin(homepage_url, js_path)

    def get_api_info(self):
        """
        JavaScript ファイル内から GraphQL Endpoint と API Key を抽出。
        設定されていない場合は例外をスローします。
        """
        javascript_url = self.get_javascript_url(Config.get_url())
        _logger.info(f"JavaScript URL: {javascript_url}")

        response = requests.get(javascript_url)
        response.raise_for_status()
        code = response.text

        endpoint_match = re.search(r'aws_appsync_graphqlEndpoint\s*:\s*"([^"]+)"', code)
        apikey_match = re.search(r'aws_appsync_apiKey\s*:\s*"([^"]+)"', code)

        if not endpoint_match:
            raise RuntimeError("GraphQL Endpointが見つかりませんでした。")
        if not apikey_match:
            raise RuntimeError("API Keyが見つかりませんでした。")

        self.graphql_endpoint = endpoint_match.group(1)
        self.api_key = apikey_match.group(1)

        _logger.info(f"GraphQL Endpoint: {self.graphql_endpoint}")
        _logger.info(f"API Key: {self.api_key}")

    def fetch_data(self, payload: dict) -> dict:
        """
        GraphQL エンドポイントに POST でデータを送信し、レスポンス JSON を返します。
        :param payload: GraphQL クエリペイロード
        """
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

        response = requests.post(self.graphql_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

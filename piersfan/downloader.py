import os
import time
import logging
import datetime
import urllib
import urllib.request
import toml
from http.client import IncompleteRead
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from piersfan import config
from piersfan.config import Config

Description = '''
フィッシングピアースの釣果情報ホームページをダウンロードする
'''


_logger = logging.getLogger(__name__)


class Download:
    def __init__(self, max_page=config.MaxPage):
        """
        ホームページダウンロードパラメータを初期化します
        """
        self.areas = []
        self.now = datetime.date.today()
        self.crawl_interval = config.CrawlInterval
        self.max_page = max_page
        self.page_found = True

    def load_config(self, config_path=Config.get_config_path()):
        """
        設定ファイルを読み、ホームページダウンロードパラメータを登録します
        """
        config_toml = toml.load(open(config_path, encoding='utf-8'))
        if 'area' in config_toml:
            self.areas = config_toml.get('area')
        if 'interval' in config_toml:
            self.crawl_interval = config_toml['interval']
        if 'max_page' in config_toml:
            self.max_page = config_toml['max_page']
        return self

    def check_config(self):
        """
        設定値のチェック
        """
        if len(self.areas) == 0:
            _logger.error("download area list is empty")
            return None
        elif self.crawl_interval < config.CrawlInterval:
            _logger.error("crawl interval must be greater than {}".
                format(config.CrawlInterval))
            return None
        return self

    def reset_download(self):
        """
        SQLite3 データベースファイルを削除します
        """
        download_dir = Config.get_download_path("")
        _logger.info("initialize {}".format(download_dir))
        download_files = os.listdir(download_dir)
        for download_file in download_files:
            if download_file.endswith(".html"):
                os.remove(os.path.join(download_dir, download_file))        

    def get_query_times(self, delta_month):
        """
        現在時刻から指定カ月の過去の年、月を返します。値はホームページ検索
        条件に使用します
        """
        date = self.now - relativedelta(months=delta_month)
        return [date.year, date.month]

    @staticmethod
    def get_form_data(year, month, page=1):
        """
        検索フォームデータを作成します
        """
        values = dict(page=page, choko_ys=year, choko_ms='{:0=2}'.format(month))
        data = urllib.parse.urlencode(values)
        return data.encode('ascii')  # data should be bytes

    def check_html_no_data(self, html_data):
        """
        取得した HTML に釣果ページがあるか判定します
        """
        self.page_found = True
        soup = BeautifulSoup(html_data, 'html.parser')
        contents = soup.find_all('div', class_="choka")
        if not contents:
            self.page_found = False
        return self

    def download(self, area_name, year, month, page=1):
        """
        指定した検索条件でホームページをダウンロードして、CSV に保存します
        """
        download_url = Config.get_url(area_name)
        download_file = Config.get_download_file(area_name, year, month, page)
        save_path = Config.get_download_path(download_file)
        if os.path.exists(save_path):
            _logger.info("skip download for file exist {}".format(download_file))
            return

        form_data = self.get_form_data(year, month, page)
        req = urllib.request.Request(download_url, form_data)
        try:
            html_data = urllib.request.urlopen(req).read()
        except IncompleteRead as e:
            html_data = e.partial
        time.sleep(self.crawl_interval)

        self.check_html_no_data(html_data)
        if self.page_found:
            with open(save_path, mode="wb") as f:
                f.write(html_data)
            _logger.info("save {}".format(download_file))

    def run(self, last_month=0, keep=False):
        """
        各施設のホープページを巡回して、ダウンロードした結果を CSV に保存します
        """
        if not keep:
            self.reset_download()
        for area in self.areas:
            area_name = area['name']
            delta_month = last_month
            while delta_month >= 0:
                [year, month] = self.get_query_times(delta_month)
                _logger.info("post a search request for {} in {}/{}".format(
                    area_name, year, month))
                page = 1
                while page <= self.max_page:
                    self.download(area_name, year, month, page)
                    page = page + 1
                    if not self.page_found:
                        break
                delta_month = delta_month - 1

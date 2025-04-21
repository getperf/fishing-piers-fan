import pytest
import re
from unittest.mock import patch, MagicMock
from piersfan.extractor import Extractor

# py.test tests/test_extractor.py -v --capture=no 


@pytest.fixture
def extractor():
    return Extractor()


def test_get_javascript_url_success(extractor):
    html = """
  <html><head><script type="module" src="/static/main.js"></script></head></html>
  """
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        url = extractor.get_javascript_url("https://example.com")
        assert url == "https://example.com/static/main.js"


def test_get_javascript_url_no_script(extractor):
    html = "<html><head></head></html>"
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        with pytest.raises(
            RuntimeError, match="JavaScriptファイルが見つかりませんでした"
        ):
            extractor.get_javascript_url("https://example.com")


def test_get_api_info_success(extractor):
    js_code = """
  const config = {
      aws_appsync_graphqlEndpoint: "https://graphql.example.com/api",
      aws_appsync_apiKey: "ABC123XYZ"
  };
  """
    with patch(
        "piersfan.extractor.Config.get_url", return_value="https://example.com"
    ), patch("requests.get") as mock_get:
        mock_homepage = MagicMock()
        mock_homepage.status_code = 200
        mock_homepage.text = '<script type="module" src="/app.js"></script>'

        mock_js = MagicMock()
        mock_js.status_code = 200
        mock_js.text = js_code

        mock_get.side_effect = [mock_homepage, mock_js]

        extractor.get_api_info()
        assert extractor.graphql_endpoint == "https://graphql.example.com/api"
        assert extractor.api_key == "ABC123XYZ"


def test_fetch_data_success(extractor):
    extractor.graphql_endpoint = "https://graphql.example.com/api"
    extractor.api_key = "TESTKEY"

    expected_response = {"data": {"hello": "world"}}
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        result = extractor.fetch_data({"query": "{ hello }"})
        assert result == expected_response

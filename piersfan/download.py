import time
import logging
import datetime
import urllib
import urllib.request
import toml
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from piersfan import config
from piersfan.config import Config

Description = '''
横浜フィッシングピアースの釣果情報ホームページをダウンロードする
'''

# UrlFishingPiers = "http://{}.yokohama-fishingpiers.jp/choka.php"
# CrawlInterval = 5
# DownloadDir = 'download'

_logger = logging.getLogger(__name__)

class Download:
    def __init__(self):
        self.areas = dict()
        self.now = datetime.date.today()
        self.crawl_interval = config.CrawlInterval
        self.max_page = config.MaxPage
        self.page_found = True

    def load_config(self, config_path='config.toml'):
        config_toml = toml.load(config_path)
        if 'area' in config_toml:
            self.areas = config_toml['area']
        if 'interval' in config_toml:
            self.crawl_interval = config_toml['interval']
        if 'max_page' in config_toml:
            self.max_page = config_toml['max_page']

        _logger.info("area load : {}".format(self.areas))
        return self

    def get_query_times(self, delta_month):
        date = self.now - relativedelta(months=delta_month)
        return [date.year, date.month]

    def get_form_data(self, year, month, page=1):
        values = dict(page=page, choko_ys=year, choko_ms='{:0=2}'.format(month))
        data = urllib.parse.urlencode(values)
        return data.encode('ascii')  # data should be bytes

    def check_html_no_data(self, html_data):
        self.page_found = True
        soup = BeautifulSoup(html_data, 'html.parser')
        contents = soup.find_all('div', class_="choka")
        if not contents:
            self.page_found = False
        return self

    def download(self, area_name, year, month, page=1):
        download_url = Config.get_url(area_name)
        download_file = Config.get_download_file(area_name, year, month, page)
        save_path = Config.get_download_path(download_file)

        form_data = self.get_form_data(year, month, page)
        req = urllib.request.Request(download_url, form_data)
        html_data = urllib.request.urlopen(req).read()
        self.check_html_no_data(html_data)
        if self.page_found:
            with open(save_path, mode="wb") as f:
                f.write(html_data)
            _logger.info("download: {}".format(download_file))

    def run(self, last_month=0):
        for area in self.areas:
            area_name = area['name']
            delta_month = last_month
            while delta_month >= 0:
                _logger.info("URL:{}".format(Config.get_url(area_name)))
                [year, month] = self.get_query_times(delta_month)
                page = 1
                while page <= self.max_page:
                    self.download(area_name, year, month, page)
                    time.sleep(self.crawl_interval)
                    page = page + 1
                    if not self.page_found:
                        break
                delta_month = delta_month - 1

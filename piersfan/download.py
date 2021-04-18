import time
import urllib
import toml

from piersfan import config
from piersfan.config import Config

Description = '''
横浜フィッシングピアースの釣果情報ホームページをダウンロードする
'''

# UrlFishingPiers = "http://{}.yokohama-fishingpiers.jp/choka.php"
CrawlInterval = 5
DownloadDir = 'download'


class Download:
    def __init__(self):
        self.areas = dict()
        self.crawl_interval = config.CrawlInterval

    def load_config(self, config_path='config.toml'):
        config_toml = toml.load(config_path)
        if config_toml['area']:
            self.areas = config_toml['area']
        if config_toml['interval']:
            self.crawl_interval = config_toml['interval']

        print("area load : {}".format(self.areas))
        return self

    @staticmethod
    def get_download_file(name, year, month, page=1):
        return 'choka_{}_{}_{:0=2}_{:0=3}.html'.format(name, year, month, page)

    def download(self, area_name, year, month, page=1):
        download_url = Config.get_url(area_name)
        download_file = self.get_download_file(area_name, year, month, page)
        save_path = Config.get_download_path(download_file)

        values = dict(page=page, choko_ys=year, choko_ms='{:0=2}'.format(month))
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # data should be bytes
        req = urllib.request.Request(download_url, data)
        data = urllib.request.urlopen(req).read()
        with open(save_path, mode="wb") as f:
            f.write(data)
        print("download area:{}, date:{}/{}, page:{}".format(area_name, year, month, page))

    def run(self, last_month=3):
        for area in self.areas:
            area_name = area['name']
            area_id = area['id']
            last_page = area['last_page']
            for page in range(1, last_page):
                self.download(area_name, area_id, page)
                time.sleep(self.crawl_interval)

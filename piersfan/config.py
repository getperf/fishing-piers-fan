import re
import pkg_resources

Description = '''
フィッシングピアーズ釣果情報抽出パラメータ
データ保存ディレクトリパスは Python パッケージディレクトリで管理します
'''


# フィッシングTV釣果情報ホームページURL

UrlFishingPiers = "https://yokohama-fishingpiers.jp/"

# HTMLダウンロードファイル保存場所

DownloadDir = 'download'

# CSV, SQLite3 データファイル保存場所

DataDir = 'data'

# 釣果情報を保存するデータベースファイル名

ChokaDB = 'fishing_result.db'

# ダウンロード巡回のインターバル(秒)

CrawlInterval = 3

# 釣果サイトページネーションの最大ページ数

MaxPage = 1000

# 魚種別釣果カラム

header_choka = ['Date', 'Point', 'Species', 'Count', 'SizeMin', 'SizeMax', 'WeightMin', 'WeightMax', 'Comment', 'Place']

# コメントカラム

header_comment = ['Date', 'Point', 'Weather', 'WaterTemp', 'Quantity', 'Comment']

# ニュースラインカラム

header_newsline = ['Date', 'Time', 'Point', 'Comment']

# 施設リスト

facilities = ['honmoku', 'daikoku', 'isogo']

class Config:

    @staticmethod
    def _get_path(package, filename):
        return pkg_resources.resource_filename(package, filename)

    @staticmethod
    def get_datastore_path(filename):
        return Config._get_path("data.datastore", filename)

    @staticmethod
    def get_csv(filename, facility):
        return "{}_{}.csv".format(filename, facility)

    @staticmethod
    def get_csv_path(filename, facility):
        return Config.get_datastore_path(Config.get_csv(filename, facility))

    @staticmethod
    def get_export_path(tablename):
        filename = "{}.csv".format(tablename)
        return Config._get_path("data.export", filename)

    @staticmethod
    def get_download_path(filename):
        return Config._get_path("data.download", filename)

    @staticmethod
    def test_resource(filename):
        return Config._get_path("tests.resources", filename)

    @staticmethod
    def get_url():
        return UrlFishingPiers

    @staticmethod
    def get_facilities():
        return facilities

    @staticmethod
    def get_download_file(area_name, year, month, page=1):
        return 'choka_{}_{}_{:0=2}_{:0=3}.html'.format(area_name, year, month, page)

    @staticmethod
    def get_db_path(db_file=ChokaDB):
        return Config._get_path("data", db_file)

    @staticmethod
    def get_config_path(config_file='config.toml'):
        return Config._get_path("data", config_file)

    @staticmethod
    def get_ap_log_path(log_file='yfp.log'):
        return Config._get_path("data", log_file)

    @staticmethod
    def list_download_dirs():
        return pkg_resources.resource_listdir('data', 'download')

    @staticmethod
    def get_point_from_html_filename(html_file):
        m = re.match(r'choka_(.+)_(\d+)_(\d+)_(\d+)\.html$', html_file)
        if m:
            [point, year, month, page] = m.groups()
            return point
        return None

    @staticmethod
    def show_config():
        print("database={}".format(Config.get_db_path()))
        print("config={}".format(Config.get_config_path()))
        print("download={}".format(Config.get_download_path("")))

import pkg_resources

# フィッシングTV釣果情報ホームページURL

UrlFishingPiers = "http://{}.yokohama-fishingpiers.jp/choka.php"

# HTMLダウンロードファイル保存場所

DownloadDir = 'download'

# CSV, SQLite3 データファイル保存場所

DataDir = 'data'

# 釣果情報を保存するデータベースファイル名

ChokaDB = 'fishing_result.sqlite3'

# ダウンロード巡回のインターバル(秒)

CrawlInterval = 5

# 魚種別釣果カラム

header_choka = ['Date', 'Point', 'Species', 'Count', 'SizeMin', 'SizeMax', 'WeightMin', 'WeightMax', 'Comment', 'Place']

# コメントカラム

header_comment = ['Date', 'Point', 'Weather', 'WaterTemp', 'Quantity', 'Comment']

# ニュースラインカラム

header_newsline = ['Date', 'Time', 'Point', 'Comment']


class Config:

    @staticmethod
    def _get_path(package, filename):
        return pkg_resources.resource_filename(package, filename)

    @staticmethod
    def get_data_path(filename):
        return Config._get_path("data", filename)

    @staticmethod
    def get_download_path(filename):
        return Config._get_path("download", filename)

    @staticmethod
    def test_resource(filename):
        return Config._get_path("tests.resources", filename)

    @staticmethod
    def get_url(area_name):
        return UrlFishingPiers.formant(area_name)

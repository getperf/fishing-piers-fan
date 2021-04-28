from piersfan.download import Download
from piersfan.config import Config


# py.test tests/test_download.py -v --capture=no -k test_run

# 施設ごとに順に巡回する
# 何カ月前からダウンロードするかを指定
# URL フォームデータに年、月を指定し、開始月から順にアクセス
# 各ページをダウンロード
#     ページの解析結果で 「データがありません」がでたら、翌月にカウントアップ
#     最終更新日付を記録する
#     巡回して取得したページの日付が前回の最終更新日付よりも古ければ終了する

def test_get_url():
    assert Config.get_url("daikoku") == 'http://daikoku.yokohama-fishingpiers.jp/choka.php'


def test_get_download_file():
    assert Config.get_download_file("daikoku", 2021, 4) == "choka_daikoku_2021_04_001.html"


def test_html_no_data():
    html_path = Config.test_resource("not_found1.html")
    f = open(html_path, encoding='euc_jp', errors='ignore')
    html = f.read()
    f.close()
    download = Download().load_config().check_html_no_data(html)
    assert not download.page_found


def test_run():
    download = Download().load_config()
    download.run(0)

# def test_getFormData():
#     download = Download()
#     assert download.getFormData(2021, 3) == 'page=1&choko_ys=2021&choko_ms=03'

# def test_getDownloadFile():
#     download = Download()
#     assert download.get_download_file('daikoku', 2021, 3, 1) == 'choka_daikoku_2021_03_001.html'

# def test_download():
#     download = Download()
#     assert download.download('daikoku', 2021, 3, 1) == None

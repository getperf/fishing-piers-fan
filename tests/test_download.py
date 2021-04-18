import re
import sys
import os
import pytest
import datetime
import pandas as pd
from piersfan.download import Download

# py.test tests/test_download.py -v --capture=no -k test_download

# 施設ごとに順に巡回する
# 何カ月前からダウンロードするかを指定
# URL フォームデータに年、月を指定し、開始月から順にアクセス
# 各ページをダウンロード
#     ページの解析結果で 「データがありません」がでたら、翌月にカウントアップ
#     最終更新日付を記録する
#     巡回して取得したページの日付が前回の最終更新日付よりも古ければ終了する

def test_getUrl():
    download = Download()
    assert download.getUrl("daikoku") == 'http://daikoku.yokohama-fishingpiers.jp/choka.php'

def test_getFormData():
    download = Download()
    assert download.getFormData(2021, 3) == 'page=1&choko_ys=2021&choko_ms=03'

def test_getDownloadFile():
    download = Download()
    assert download.get_download_file('daikoku', 2021, 3, 1) == 'choka_daikoku_2021_03_001.html'

def test_download():
    download = Download()
    assert download.download('daikoku', 2021, 3, 1) == None



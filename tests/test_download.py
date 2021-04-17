import re
import sys
import os
import pytest
import datetime
import pandas as pd
from piersfan.download import Download

# py.test tests/test_download.py -v --capture=no -k test_download

def test_getUrl():
    download = Download()
    assert download.getUrl("daikoku") == 'http://daikoku.yokohama-fishingpiers.jp/choka.php'

def test_getFormData():
    download = Download()
    assert download.getFormData(2021, 3) == 'page=1&choko_ys=2021&choko_ms=03'

def test_getDownloadFile():
    download = Download()
    assert download.getDownloadFile('daikoku', 2021, 3, 1) == 'choka_daikoku_2021_03_001.html'

def test_download():
    download = Download()
    assert download.download('daikoku', 2021, 3, 1) == None



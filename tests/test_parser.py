import re
import sys
import os
import pytest
import datetime
import pandas as pd
import pkg_resources
from importlib.resources import read_text
import importlib
from piersfan.parser import Parser
from logging import INFO, ERROR, getLogger

# logger = getLogger('test')

# py.test tests/test_parser.py -v --capture=no -k test_daikoku_html_parseer

def get_test_data(filename):
    return pkg_resources.resource_filename("tests.resources", filename)

def test_not_found():
    html_path = get_test_data("not_found1.html")
    parser = Parser("daikoku", 2021, 4, 9999)
    parser.parse_html(html_path) == None

def test_daikoku_html_parseer(caplog):
    # caplog.set_level(INFO)

    html_path = get_test_data("daikoku1.html")
    parser = Parser("daikoku", 2021, 4, 1).parse_html(html_path)
    print(parser.choka_comment)
    # parser = Parser()
    # assert parser.getWaterTemp("【水温】14℃") == 14.0
    # assert parser.getWaterTemp("【水温】15.3℃") == 15.3
    # assert parser.getWaterTemp("【水温】") == None

# def test_getChokaDate():
#     parser = Parser()
#     assert parser.getChokaDate("2021年4月2日( )") == datetime.datetime(2021, 4, 2, 0, 0)

# def test_convertValue():
#     parser = Parser()
#     assert parser.convertValue("合計 13匹") == 13.0
#     assert parser.convertValue("25～30 cm") == [25, 30]



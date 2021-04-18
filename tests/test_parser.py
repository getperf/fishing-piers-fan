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
    Parser("daikoku", 2021, 4, 9999).parse_html(html_path) == None

def test_daikoku_html_parseer():
    html_path = get_test_data("daikoku1.html")
    parser = Parser("daikoku", 2021, 4).parse_html(html_path)
    timestamps = parser.get_timestamps()
    print(parser.choka.columns)
    print(parser.comment.columns)
    print(parser.newsline.columns)
    assert timestamps['choka'] != None
    assert timestamps['newsline'] != None

def test_daikoku_only_newsline_parseer():
    html_path = get_test_data("daikoku1_newsline.html")
    parser = Parser("daikoku", 2021, 4).parse_html(html_path)
    timestamps = parser.get_timestamps()
    assert timestamps['choka'] == None
    assert timestamps['newsline'] != None

def test_isogo_html_parseer():
    html_path = get_test_data("isogo1.html")
    parser = Parser("isogo", 2021, 4).parse_html(html_path)
    timestamps = parser.get_timestamps()
    print(timestamps)
    assert timestamps['choka'] != None
    assert timestamps['newsline'] != None

def test_honmoku_html_parseer():
    html_path = get_test_data("honmoku1.html")
    parser = Parser("honmoku", 2021, 4).parse_html(html_path)
    timestamps = parser.get_timestamps()
    print(timestamps)
    assert timestamps['choka'] != None
    assert timestamps['newsline'] != None

def test_export():
    html_path = get_test_data("daikoku1.html")
    parser = Parser("daikoku", 2021, 4).parse_html(html_path)
    parser.export('csv')

def test_append():
    html_path = get_test_data("daikoku1.html")
    parser = Parser("daikoku", 2021, 4).parse_html(html_path)
    html_path2 = get_test_data("isogo1.html")
    parser2 = Parser("isogo", 2021, 4).parse_html(html_path2)
    parser.append(parser2)
    timestamps = parser.get_timestamps()
    print(timestamps)
    assert timestamps['choka'] != None
    assert timestamps['newsline'] != None

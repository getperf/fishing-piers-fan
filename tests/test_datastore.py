import re
import sys
import os
import pytest
import datetime
import pkg_resources
import pandas as pd
from piersfan.parser import Parser
from piersfan.datastore import Datastore
from tests.test_parser import get_test_data

# py.test tests/test_datastore.py -v --capture=no -k test_reset_loadfile

TEST_DB = 'test_fishing_result.db'

def test_init():
    Datastore(TEST_DB).reset_database()
    db_path = pkg_resources.resource_filename("data", "fishing_result.db")
    os.path.exists(db_path) == False

def test_reset_loadfile():
    datastore = Datastore(TEST_DB).reset_loadfiles()
    datastore.load_counts == {'choka.csv': 0, 'comment.csv': 0, 'newsline.csv': 0}

def test_initial_export():
    datastore = Datastore(TEST_DB).reset_database()
    html_path = get_test_data("daikoku1.html")
    parser = Parser("daikoku", 2021, 4).parse_html(html_path)
    parser.export('csv')
    datastore.csv_import()
    datastore.load_counts == {'choka.csv': 12, 'comment.csv': 1, 'newsline.csv': 9}

def test_append_load():
    datastore = Datastore(TEST_DB).reset_database()
    parser = Parser("daikoku", 2021, 4).parse_html(get_test_data("daikoku1.html"))
    parser.export('csv')
    datastore.csv_import()

    parser2 = Parser("isogo", 2021, 4).parse_html(get_test_data("isogo1.html"))
    parser2.export('csv')
    datastore.csv_import()
    datastore.load_counts['choka.csv'] == 19

    parser3 = Parser("honmoku", 2021, 4).parse_html(get_test_data("honmoku1.html"))
    parser3.export('csv')
    datastore.csv_import()
    datastore.load_counts['choka.csv'] == 54

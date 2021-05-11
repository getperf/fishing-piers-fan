import os
import sys
import pytest

from piersfan.config import Config
from piersfan.datastore import Datastore
from piersfan.parser import Parser

# py.test tests/test_datastore.py -v --capture=no -k test_get_choka_db

TEST_DB = 'test_fishing_result.db'


def test_init():
    Datastore(TEST_DB).reset_database()
    db_path = Config.get_db_path(TEST_DB)
    assert not os.path.exists(db_path)


def test_get_choka_db():
    print(Config.get_db_path())


def test_reset_loadfile():
    datastore = Datastore(TEST_DB).reset_load_files()
    assert datastore.load_counts == {'choka.csv': 0, 'comment.csv': 0, 'newsline.csv': 0}

@pytest.mark.skipif(sys.platform == 'win32',
                    reason="does not run on windows")
def test_initial_export():
    datastore = Datastore(TEST_DB).reset_database()
    html_path = Config.test_resource("daikoku1.html")
    parser = Parser("daikoku").parse_html(html_path)
    parser.export('csv')
    datastore.csv_import()
    assert datastore.load_counts == {'choka.csv': 12, 'comment.csv': 1, 'newsline.csv': 9}


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="does not run on windows")
def test_append_load():
    datastore = Datastore(TEST_DB).reset_database()
    parser = Parser("daikoku").parse_html(Config.test_resource("daikoku1.html"))
    parser.export('csv')
    datastore.csv_import()

    parser2 = Parser("isogo").parse_html(Config.test_resource("isogo1.html"))
    parser2.export('csv')
    datastore.csv_import()
    assert datastore.load_counts['choka.csv'] == 19

    parser3 = Parser("honmoku").parse_html(Config.test_resource("honmoku1.html"))
    parser3.export('csv')
    datastore.csv_import()
    assert datastore.load_counts['choka.csv'] == 54

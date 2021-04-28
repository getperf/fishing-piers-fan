from piersfan.config import Config


# py.test tests/test_config.py -v --capture=no -k test_get_path

def test_get_path():
    assert Config.get_datastore_path("choka.csv")
    assert Config.get_download_path("choka_daikoku_2021_04_001.html")
    assert Config.test_resource("daikoku1.html")
    assert Config.get_url("daikoku")
    assert Config.get_download_file("daikoku", 2021,4)
    assert Config.get_db_path()
    assert Config.get_config_path("config.toml")

def test_get_point_from_html_filename():
    assert Config.get_point_from_html_filename("choka_daikoku_2021_04_001.html") == "daikoku"
    assert Config.get_point_from_html_filename("hoge.html") == None

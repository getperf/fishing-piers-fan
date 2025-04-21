import toml
import pandas as pd
from piersfan.config import Config


# py.test tests/test_config.py -v --capture=no -k test_toml_multibyte

def test_get_path():
    assert Config.get_datastore_path("choka.csv")
    assert Config.get_download_path("choka_daikoku_2021_04_001.html")
    assert Config.test_resource("daikoku1.html")
    assert Config.get_url()
    assert Config.get_download_file("daikoku", 2021,4)
    assert Config.get_db_path()
    assert Config.get_config_path("config.toml")

def test_get_point_from_html_filename():
    assert Config.get_point_from_html_filename("choka_daikoku_2021_04_001.html") == "daikoku"
    assert Config.get_point_from_html_filename("hoge.html") == None

def test_toml_multibyte():
    config_path = Config.get_config_path("config.toml")
    config_toml = toml.load(open(config_path, encoding='utf-8'))
    df = pd.DataFrame(columns=['Target', 'Species'])

    if 'target' in config_toml:
        targets = config_toml['target']
        for target in targets:
            target_name = target['name']
            for species in target['species']:
                values = {'Target': target_name, 'Species': species}
                df = pd.concat(
                    [df, pd.DataFrame([values])],
                    ignore_index=True
                )
    print(df)
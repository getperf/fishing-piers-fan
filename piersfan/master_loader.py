import os
import re
import logging
import datetime
import sqlite3
import toml
import pandas as pd
import dataset as ds
from piersfan import config
from piersfan.config import Config
from piersfan.converter import Converter
from piersfan.datastore import Datastore

Description = '''
config.tomlに定義したマスターデータを SQLite3 にインポートします。
'''

_logger = logging.getLogger(__name__)


class MasterLoader:
    def __init__(self, db_name=config.ChokaDB):
        """
        SQLite3 データベースへの接続と、各モデル定義を初期化します
        """
        self.db_path = Config.get_db_path(db_name)
        # self.db = sqlite3.connect('sqlite:///{}'.format(self.db_path))
        self.db = sqlite3.connect(self.db_path)
        self.target = pd.DataFrame(columns=['Target', 'Species'])
        self.area = pd.DataFrame(columns=['Point', 'PointName'])

    def load_config(self, config_path=Config.get_config_path()):
        """
        設定ファイルを読み、ホームページダウンロードパラメータを登録します
        """
        config_toml = toml.load(open(config_path, encoding='utf-8'))

        """魚種ターゲットの読み込み"""
        if 'target' in config_toml:
            targets = config_toml['target']
            for target in targets:
                target_name = target['name']
                for species in target['species']:
                    values = {'Target': target_name, 'Species': species}
                    self.target = pd.concat(
                        [self.target, pd.DataFrame([values])],
                        ignore_index=True
                    )

        """魚種ターゲットの読み込み"""
        if 'area' in config_toml:
            areas = config_toml['area']
            for area in areas:
                values = {
                    'Point': area['name'],
                    'PointName': area['label']
                }
                new_row_df = pd.DataFrame([values])  # 新しい行をDataFrameに変換
                self.area = pd.concat(
                    [self.area, new_row_df],
                    ignore_index=True
                )

        return self

    def check_config(self):
        """
        設定値のチェック
        """
        return self

    def initial_load(self):
        """
        テーブルを作成し、データフレームをロード(上書き更新)します
        """
        if len(self.target) > 0:
            self.target.to_sql("fishing_target", self.db, if_exists="replace")
        if len(self.area) > 0:
            self.area.to_sql("fishing_area", self.db, if_exists="replace")

    def run(self):
        """
        SQLite3 から指定した期間の履歴データをCSVにエクスポートします
        """
        _logger.info("load fishing_target {} row".format(len(self.target)))
        _logger.info("load fishing_area {} row".format(len(self.area)))
        self.initial_load()

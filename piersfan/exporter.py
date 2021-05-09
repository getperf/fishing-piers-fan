import os
import re
import logging
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import dataset as ds
from piersfan import config
from piersfan.config import Config
from piersfan.converter import Converter
from piersfan.datastore import Datastore

Description = '''
SQLite3から、csv データをエクスポートします。
'''

_logger = logging.getLogger(__name__)


class Exporter:
    def __init__(self, db_name=config.ChokaDB):
        """
        SQLite3 データベースへの接続と、各モデル定義を初期化します
        """
        self.db_path = Config.get_db_path(db_name)
        self.db = ds.connect('sqlite:///{}'.format(self.db_path))

    def get_last_time(self, interval):
        """
        1day,1month,1year を引数に過去の日付を計算する
        """
        m = re.search(r'([0-9]+)(day|month|year)', interval)
        if not m:
            return None
        [interval, unit] = m.groups()

        today = datetime.datetime.now()
        if unit == "day":
            return today - relativedelta(days = int(interval))
        elif unit == "month":
            return today - relativedelta(months = int(interval))
        elif unit == "year":
            return today - relativedelta(years = int(interval))

    def cleansing_data(self, table_name, df):
        """
        分析に不要なデータを取り除いて整形する
        """
        if table_name == 'fishing_comments':
            df['Comment'] = df['Comment'].map(Converter.clensing_summary_comment)
        if table_name == 'fishing_newslines':
            df['Comment'] = df['Comment'].map(Converter.clensing_newsline_comment)
        return df

    def run(self, interval):
        """
        SQLite3 から指定した期間の履歴データをCSVにエクスポートします
        """
        last_timestamp = self.get_last_time(interval)
        if not last_timestamp:
            _logger.error(
                "--time parse {} by 'n[day|month|yaer]'".format(
                interval))
            return None

        last_date = last_timestamp.strftime('%Y-%m-%d')
        ds = Datastore()
        for table_name in ds.get_table_names():
            sql = "select * from {} where Date >= :start".format(
                table_name)
            df = pd.read_sql_query(sql,
                                   index_col=['Date'], 
                                   con=ds.db.engine, 
                                   params={"start":last_date})
            df = df.drop(columns=['index'])
            df = self.cleansing_data(table_name, df)
            export_path = Config.get_export_path(table_name)
            df.to_csv(export_path)
            _logger.info("save {}".format(export_path))


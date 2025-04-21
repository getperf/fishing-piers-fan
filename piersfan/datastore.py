import os
import logging
import pandas as pd
import dataset as ds
from piersfan import config
from piersfan.config import Config

Description = '''
SQLite3を用いて釣果情報を管理します。
フィッシングピアーズ釣果情報ホームページから釣果を取得した、
csv データをインポートします。
'''

_logger = logging.getLogger(__name__)


class Table:
    def __init__(self, table_name, index_columns, rows, csv):
        """
        データベースに登録するモデルの属性を定義します
        """
        self.table_name = table_name
        self.index_columns = index_columns
        self.csv = csv
        self.rows = rows


class Datastore:
    def __init__(self, db_name=config.ChokaDB):
        """
        SQLite3 データベースへの接続と、各モデル定義を初期化します
        """
        self.db_path = Config.get_db_path(db_name)
        db = ds.connect('sqlite:///{}'.format(self.db_path))
        self.db = db
        self.tables = [
            Table('fishing_results', 
                ['Date', 'Point', 'Species'], 
                dict(index=0, Date="", Point="", Species="", 
                    Count=0.0, SizeMin=0.0, SizeMax=0.0, 
                    WeightMin=0.0, WeightMax=0.0, Comment="", Place=""),
                'choka'),
            Table('fishing_comments', 
                ['Date', 'Point'], 
                dict(index=0, Date="", Point="", Weather="", 
                    WaterTemp=0.0, Quantity=0.0, 
                    Comment="", Tide="", Time="", Summary="", BizDay=""),
                'comment'),
            Table('fishing_newslines', 
                ['Date', 'Time', 'Point'], 
                dict(index=0, Date="", Time="", Point="", Comment="", Weather=""),
                'newsline'),
        ]
        self.load_counts = dict()

    def get_table_names(self):
        """
        テーブル名のリストを返します
        """
        table_names = list()
        for table in self.tables:
            table_names.append(table.table_name)
        return table_names

    def reset_load_file(self, filename):
        """
        CSV ロードファイルを削除します
        """
        load_path = Config.get_datastore_path(filename)
        if os.path.exists(load_path):
            os.remove(load_path)
        self.load_counts[filename] = 0

    def reset_load_files(self):
        """
        各 CSV ロードファイルを削除します
        """
        for table in self.tables:
            self.reset_load_file(table.csv)
        return self

    def reset_database(self):
        """
        SQLite3 データベースファイルを削除し、再作成します
        """
        _logger.info("initialize {}".format(self.db_path))
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        """Table.rows のカラム定義を基にテーブルを作成します。
        dataset.insert(columns)でテーブルの作成をしますが、カラム値がNoneの場合は、
        テキストのカラムでも誤ってFloat 型で初期化されてしまいます。
        回避するために一旦、Table.rowsで定義されたレコードを登録して、テーブル
        を作成し、その後レコードを削除する処理を追加します。"""
        for table in self.tables:
            tbl = self.db[table.table_name]
            tbl.insert(table.rows)
            tbl.delete()
        return self

    def create_index(self, table_name, index_columns):
        """
        テーブルに索引を追加します
        """
        self.db.create_table(table_name).create_index(index_columns)

    def create_indexes(self):
        """
        各テーブルに索引を追加します
        """
        for table in self.tables:
            self.create_index(table.table_name, table.index_columns)

    def initial_load(self, csv, table_name):
        """
        テーブルを作成して、CSV データを初期ロードをします
        """
        results = pd.read_csv(Config.get_datastore_path(csv), index_col=0)
        results.to_sql(table_name, self.db.engine, if_exists="replace")
        self.load_counts[csv] = len(results.index)

    def initial_loads(self):
        """
        各テーブルを作成して、CSV データを初期ロードをします
        """
        self.reset_database()
        for table in self.tables:
            self.initial_load(table.csv, table.table_name)

        _logger.info("initial load : {}".format(self.load_counts))
        self.create_indexes()

    def upsert_row(self, table_name, index_columns, values):
        """
        テーブルにレコードを追加します、既設のレコードは更新します
        """
        table = self.db[table_name]
        keys = dict()
        for index_column in index_columns:
            keys[index_column] = values[index_column]
        if table.find_one(**keys):
            table.update(values, index_columns)
        else:
            table.insert(values)

    def append_load(self, csv_file, table_name, index_columns):
        """
        テーブルに全 CSV レコードを登録します、既設のレコードは更新します
        """
        csv_path = Config.get_datastore_path(csv_file)
        results = pd.read_csv(csv_path)
        for result in results.to_dict(orient='records'):
            self.upsert_row(table_name, index_columns, result)
        self.load_counts[csv_file] = len(results.index)
        return self

    def append_loads(self):
        """
        各テーブルに全 CSV レコードを登録します、既設のレコードは更新します
        """
        for table in self.tables:
            for facility in Config.get_facilities():
                csv_file = Config.get_csv(table.csv, facility)
                self.append_load(csv_file, table.table_name, table.index_columns)
        _logger.info("upsert load : {}".format(self.load_counts))
        return self

    def csv_import(self):
        """
        データベースに各 CSV ファイルをインポートします。既設のデータベース
        がある場合は追加登録します
        """
        if os.path.exists(self.db_path):
            self.append_loads()
        else:
            self.initial_loads()

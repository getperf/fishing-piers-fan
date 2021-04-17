"""統計処理管理

SQLite3 を用いて処理統計を管理します。
指定したメトリック名に対して SQLite3 に値を登録します。
Stat().show() メソッドで、登録したメトリックをレポートします。
"""

import logging
import pandas as pd
import dataset as ds

class Datastore():
    def __init__(self):
        db = ds.connect('sqlite:///fishing_result.db')
        self.db = db
        logging.getLogger(__name__).info("database created")

    def create_indexes(self):
        results = self.db.create_table('fishing_results')
        results.create_index(['Date', 'Point', 'Species'])
        comments = self.db.create_table('fishing_comments')
        comments.create_index(['Date', 'Point'])

    def run(self):
        results = pd.read_csv('chokaData.csv', index_col = 0)
        results.to_sql("fishing_results", self.db.engine, if_exists="replace")

        comments = pd.read_csv('chokaComment.csv', index_col = 0)
        comments.to_sql("fishing_comments", self.db.engine, if_exists="replace")

        dates = pd.DataFrame({"Date": pd.date_range("2018-04-09", "2021-04-03")})
        dates['Date'] = dates.Date.dt.strftime('%Y-%m-%d')
        dates.to_sql("dates", self.db.engine, if_exists="replace")

        logging.getLogger(__name__).info("loaded")
        self.create_indexes()


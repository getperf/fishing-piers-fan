"""
横浜フィッシングピアースの釣果情報を取得する。

Parametrs
---------
-c config_paths : str[]
    コンフィグファイルパスを指定します。
-m month : int
    何カ月前のからの釣果情報ホームページをダウンロードするかを指定します。
-i init : bool
    True の場合データベースをリセットします。
"""

from datetime import datetime, timedelta
import logging
import argparse
from piersfan import config
from piersfan.config import Config
from piersfan.downloader import Download
from piersfan.extractor import Extractor
from piersfan.extractor_news_line import ExtractorNewsLine
from piersfan.extractor_summary import ExtractorSummary
from piersfan.job_status import JobStatus
from piersfan.parser import Parser
from piersfan.datastore import Datastore
from piersfan.exporter import Exporter
from piersfan.master_loader import MasterLoader


Description='''
横浜フィッシングピアースの釣果情報を取得する。
'''


_logger = logging.getLogger(__name__)

class YFPFan():

    def set_envoronment(self, args):
        """
        環境変数の初期化。以下のコードで初期化する
        """
        self.config_path = args.config
        self.day = args.day
        self.init = args.init
        self.query = args.query
        self.datastore = args.datastore
        self.log_enable = args.log
        self.show = args.show
        self.export = args.export
        self.time = args.time
        self.loadmaster = args.loadmaster

    def get_date_filter(self):
        """
        日付フィルタを取得する
        """
        date_after = datetime.now() - timedelta(days=self.day)
        if self.day > 0:
            date_after = datetime.now() - timedelta(days=self.day)
        elif JobStatus().get_last_execution_time("main"):
            date_after = datetime.strptime(
                JobStatus().get_last_execution_time("main"), '%Y-%m-%dT%H:%M:%S.%f'
            )
        return date_after.strftime('%Y/%m/%d')

    def parser(self):
        """
        コマンド実行オプションの解析
        """
        parser = argparse.ArgumentParser(description=Description)
        parser.add_argument("-c", "--config", type = str, 
                            default = Config.get_config_path(), 
                            help = "<path>\\config.toml")
        parser.add_argument("--day", type = int, default = 0, 
                            help = "last n day before downloading")
        parser.add_argument("-i", "--init", action="store_true", 
                            help = "initialize database")
        parser.add_argument("-l", "--log", action="store_true", 
                            help = "write log to file")
        parser.add_argument("-s", "--show", action="store_true", 
                            help = "show config parameter")
        parser.add_argument("-e", "--export", action="store_true",
                            help = "export csv data")
        parser.add_argument("-q", "--query", action="store_true",
                            help = "query fishing data")
        parser.add_argument("-d", "--datastore", action="store_true",
                            help = "import fishing data to database")
        parser.add_argument("--loadmaster", action="store_true",
                            help = "import master data")
        parser.add_argument("-t", "--time", type = str,
                            default="1day",
                            help = "time period to export")
        return parser.parse_args()

    def run_query(self):
        """
        釣果情報を取得する
        """
        extractor = Extractor()
        extractor.get_api_info()
        flter_date = self.get_date_filter()
        _logger.info(f"get fishing data from '{flter_date}'")

        for facility in Config.get_facilities():
            ExtractorSummary(extractor).run(facility, flter_date)
            ExtractorNewsLine(extractor).run(facility, flter_date)

    def main(self):
        """
        メイン処理。コマンド引数別に処理する
        """
        args = self.parser()
        self.set_envoronment(args)
        log_path = None
        if self.log_enable:
            log_path = Config.get_ap_log_path()
        logging.basicConfig(
            filename=log_path,
            level=getattr(logging, 'INFO'),
            format='%(asctime)s [%(levelname)s] %(module)s %(message)s',
            datefmt='%Y/%m/%d %H:%M:%S',
        )
        if self.show:
            Config.show_config()
            JobStatus().show_job_status()
            return

        elif self.loadmaster:
            loader = MasterLoader().load_config()
            if loader:
                loader.run()

        elif self.init:
            Datastore().reset_database()
            MasterLoader().load_config().run()
            Download().reset_download()
            return

        elif self.query:
            self.run_query()
            return

        elif self.datastore:
            Datastore().csv_import()
            return

        else:
            self.run_query()
            Datastore().csv_import()
            JobStatus().save_execution_time("main")
            return

if __name__ == '__main__':
    YFPFan().main()

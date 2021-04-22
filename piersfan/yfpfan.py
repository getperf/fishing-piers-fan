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

import logging
import argparse
from piersfan.config import Config
from piersfan.download import Download
from piersfan.parser import Parser
from piersfan.datastore import Datastore


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
        self.month = args.month
        self.init = args.init

    def parser(self):
        """
        コマンド実行オプションの解析
        """
        parser = argparse.ArgumentParser(description=Description)
        parser.add_argument("-c", "--config", type = str, 
                            default = Config.get_config_path(), 
                            help = "<path>\\config.toml")
        parser.add_argument("-m", "--month", type = int, default = 0, 
                            help = "last n month before downloading")
        parser.add_argument("-i", "--init", action="store_true", 
                            help = "initialize database")
        return parser.parse_args()

    def run(self, args):
        Download.load_config(self.config_path).run(self.month)
        Parser().run()
        Datastore().csv_import(self.init)

    def main(self):
        logging.basicConfig(
            level=getattr(logging, 'INFO'),
            format='%(asctime)s [%(levelname)s] %(module)s %(message)s',
            datefmt='%Y/%m/%d %H:%M:%S',
        )
        args = self.parser()
        self.set_envoronment(args)
        self.run(args)

if __name__ == '__main__':
    YFPFan().main()

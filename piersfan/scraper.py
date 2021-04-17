import requests
import logging
import argparse
from bs4 import BeautifulSoup
import csv
import pandas as pd

Description='''
釣りビジョン釣果情報ホームページから釣果を取得する。取得情報は、
過去の水温、コメント、魚種別釣果の3種
'''

class ChokaScraper():
    GETCONFIG_TIMEOUT = 1800

    def set_envoronment(self, args):
        """
        環境変数の初期化。以下のコードで初期化する

        """
        _logger = logging.getLogger(__name__)
        self.config_paths = args.config.split(',')
        self.base_config = self.config_paths[0]
        self.excel = args.excel

    def run(self):
        """
        Getconfigのインベントリ収集からDB登録までをバッチ実行する。
        """
        _logger = logging.getLogger(__name__)
        try:
            print("TEST2")
            # for config_path in self.config_paths:
            #     self.spawn_get_inventory(config_path)

            # self.spawn_regist_inventory_db()
        except Exception as e:
              print("Command error :{}".format(e.args))

    def parser(self):
        """
        コマンド実行オプションの解析
        """
        parser = argparse.ArgumentParser(description=Description)
        parser.add_argument("-c", "--config", type = str, required = True, 
                            help = "<path>\\config.groovy")
        parser.add_argument("-e", "--excel", type = str,  
                            help = "getconfig.(xlsx|toml)")
        return parser.parse_args()

    def main(self):
        logging.basicConfig(
            level=getattr(logging, 'INFO'),
            format='%(asctime)s [%(levelname)s] %(module)s %(message)s',
            datefmt='%Y/%m/%d %H:%M:%S',
        )
        args = self.parser()
        self.set_envoronment(args)
        self.run()

if __name__ == '__main__':
    ChokaScraper().main()

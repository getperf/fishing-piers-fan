import fire
import logging
from piersfan.download import Download
from piersfan.parser import Parser
from piersfan.datastore import Datastore
from piersfan.report import Report

class Cli(object):
    '''
    横浜フィッシングピアースの釣果情報を取得する。
    '''

    def download(self, config="config.toml", month=0):
        """釣りビジョンホームページから釣果ページHTMLをダウンロードする"""
        return Download().load_config(config).run(month)

    def parse(self):
        """ダウンロードしたHTMLから釣果情報を抽出し、CSVファイルに保存する"""
        return Parser().run()

    def save(self):
        """抽出した釣果情報を、SQLite3データベースに保存する"""
        return Datastore().run()

    def report(self, type="json"):
        """抽出ファイルを解析してレポートを生成する"""
        return Report().run()

def main():
    # ログの初期化
    logging.basicConfig(
        level=getattr(logging, 'INFO'),
        format='%(asctime)s [%(levelname)s] %(module)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
    )
    logger = logging.getLogger(__name__)

    fire.Fire(Cli)

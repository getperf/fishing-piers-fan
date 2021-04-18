import logging
import os
import os.path
import re
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

import piersfan.config as config
from piersfan.config import Config
from piersfan.converter import Converter

Description = '''
釣りビジョン釣果情報ホームページから釣果を取得する。取得情報は、
水温、コメント、魚種別釣果の3種
'''

_logger = logging.getLogger(__name__)

class Parser():

    choka: DataFrame
    comment: DataFrame
    newsline: DataFrame

    def __init__(self, point, year, month, page=1):
        """
        魚種別釣果、コメントのデータフレームを初期化
        """
        self.point = point
        self.year = year
        self.month = month
        self.page = page
        self.choka = pd.DataFrame(columns=config.header_choka)
        self.comment = pd.DataFrame(columns=config.header_comment)
        self.newsline = pd.DataFrame(columns=config.header_newsline)

    def parse_html(self, html_path):
        """
        釣果ホームページのファイルを読み込み、魚種別釣果、コメントのデータフレームに格納する
        """

        """
        一部のダウンロードページに CP51932 (MIXED NL) のコードが含まれる。
        CP51932 は EUC-JP に SJIS-win をミックスしたコード体系となり、
        Python だとエンコードエラーとなるため、以下 errors='ignore' 
        でエラーを無視して EUC-JP のみ読み込む
        """
        f = open(html_path, encoding='euc_jp', errors='ignore')
        html = f.read()
        f.close()
        soup = BeautifulSoup(html, 'html.parser')

        contents = soup.find_all('div', class_="choka")
        if not contents:
            return None

        """釣果コンテンツを順に解析する"""
        for content in contents:
            content_header = content.find('div', class_="choka_head")
            if not content_header:
                continue
            choka_date = Converter.get_date(content_header.text)

            content_weather = content_header.find('span', 
                class_="choka_weather")
            content_foot = content.find('div', 
                class_="choka_foot_comment")
            content_others = content_header.find_all('span', 
                class_="choka_other")

            if content_others:
                """終了記事を解析し、ヘッダと魚種別釣果を抽出"""
                headers = dict(Date=choka_date, Point=self.point)
                Converter.get_comment(content_foot.text, headers)

                if content_weather:
                    Converter.get_header(content_weather.text, headers)
                for content_other in content_others:
                    Converter.get_header(content_other.text, headers)
                _logger.info("魚種別釣果コメント読込み", headers)
                self.comment = self.comment.append(headers, ignore_index=True)

                rows = content.find_all('tr')
                df = pd.DataFrame(columns=config.header_choka)
                for row in rows:
                    values = {'Date': choka_date, 'Point': self.point, 'Species': row.find('th').text}
                    html_items = row.find_all('td')
                    if not html_items:
                        continue
                    item_texts = list(map(lambda x: x.text, html_items))
                    Converter.get_choka_table_value(item_texts.pop(0), values)
                    Converter.get_choka_table_value(item_texts.pop(0), values)
                    self.choka = self.choka.append(values, ignore_index=True)

            else:
                """各時間の釣果ニュースラインを抽出"""
                values = dict(Date=choka_date, Point=self.point)
                if content_weather:
                    Converter.get_header(content_weather.text, values)
                Converter.get_comment(content_foot.text, values)
                self.newsline = self.newsline.append(values, ignore_index=True)
        return self

    def get_timestamps(self):
        timestamps = dict(choka=None, newsline=None)
        if len(self.comment.index) > 0:
            comment_date = self.comment["Date"]
            timestamps['choka'] = comment_date.max()
        if len(self.newsline.index) > 0:
            newsline_date = self.newsline["Time"]
            timestamps['newsline'] = newsline_date.max()
        return timestamps

    def export_data(self, df, filename, format='csv'):
        export_path = Config.get_data_path(filename)
        df.to_csv(export_path)

    def export(self, format='csv'):
        self.export_data(self.choka, "choka.csv")
        self.export_data(self.comment, "comment.csv")
        self.export_data(self.newsline, "newsline.csv")

    def append(self, parser):
        self.choka = self.choka.append(parser.choka)
        self.comment = self.comment.append(parser.comment)
        self.newsline = self.newsline.append(parser.newsline)

    def run(self):
        """
        data ディレクトリ下の ダウンロード済みの釣果情報 html ファイルを順に読む。
        釣果情報を抽出して、CSV 形式にして保存する

        """
        template_dir = os.path.join(config.DownloadDir)
        parseCount = 0
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                m = re.match(r'choka_(.+)_(\d+)\.html$', file)
                if m:
                    chokaInfo = m.groups()
                    html = os.path.join(root, file)
                    self.parseHtml(html, chokaInfo[0], chokaInfo[1])
                    parseCount += 1
                    print("parse:{},{}".format(file, parseCount))
                # if parseCount > 2:
                #     break
        self.chokaData.reset_index(drop=True, inplace=True)

        path = 'chokaData.csv'
        self.chokaData.to_csv(path)
        path = 'chokaComment.csv'
        self.chokaComments.to_csv(path)

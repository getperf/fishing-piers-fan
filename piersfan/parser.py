import re
import os
import os.path
import logging
from dateutil import parser
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

import piersfan.constants as constants
from piersfan.converter import Converter

Description = '''
釣りビジョン釣果情報ホームページから釣果を取得する。取得情報は、
水温、コメント、魚種別釣果の3種
'''

_logger = logging.getLogger(__name__)
# _logger.setLevel(logging.INFO)
# logging.basicConfig(
#     level=getattr(logging, 'INFO'),
#     format='%(asctime)s [%(levelname)s] %(module)s %(message)s',
#     datefmt='%Y/%m/%d %H:%M:%S',
# )


class Parser():

    chokaData: DataFrame

    def __init__(self, point, year, month, page=1):
        """
        魚種別釣果、コメントのデータフレームを初期化
        """
        self.point = point
        self.year = year
        self.month = month
        self.page = page
        self.chokaData = pd.DataFrame(columns=constants.ChokaHeaders)
        self.chokaComments = pd.DataFrame(columns=constants.CommentHeaders)

    def parse_html(self, html_path):
        """
        釣果ホームページのファイルを読み込み、魚種別釣果、コメントのデータフレームに格納する
        """

        """
        一部のページに CP51932 (MIXED NL) のコードを使用している。
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

        """日別の釣果コンテンツを順に解析する"""
        choka_date = None
        for content in contents:
            choka_head = content.find('div', class_="choka_head")
            if not choka_head:
                continue
            choka_date = Converter.get_date(choka_head.text)
            _logger.info("choka date:", choka_date)

            headers = {'Date': choka_date}
            choka_weather = choka_head.find('span', class_="choka_weather")
            if choka_weather:
                Converter.get_header(choka_weather.text, headers)
            choka_others = choka_head.find_all('span', class_="choka_other")
            if choka_others:
                for choka_other in choka_others:
                    Converter.get_header(choka_other.text, headers)
                _logger.info("魚種別釣果とコメント読込み")
                print("INFO:", headers)
                _logger.info("header:", headers)
                rows = content.find_all('tr')
                df = pd.DataFrame(columns=constants.ChokaHeaders)
                for row in rows:
                    values = {}
                    htmlItems = row.find_all('td')
                    if not htmlItems:
                        continue
                    itemTexts = list(map(lambda x: x.text, htmlItems))
                    print("ROW:", itemTexts)
                    # itemTexts.pop(0)
                    # values['Species'] = itemTexts.pop(0)
                    # values['Count'] = Converter.getValues(itemTexts.pop(0))
                    # sizes = Converter.getRangeValues(itemTexts.pop(0))
                    # if sizes:
                    #     values['SizeMin'] = sizes[0]
                    #     values['SizeMax'] = sizes[1]
                    # weights = Converter.getRangeValues(itemTexts.pop(0))
                    # if weights:
                    #     values['WeightMin'] = weights[0]
                    #     values['WeightMax'] = weights[1]
                    df= df.append(values, ignore_index=True)


            else:
                _logger.info("コメントのみ読込み")
                _logger.info("header:", headers)
            # print(len(choka_others))
            # for choka_other in choka_others:
            #     print("INFO:", choka_other)
            continue
            chokaTable = content.find_all('tr')

            # 魚種別釣果テーブルの抽出
            # 入力例 1:タコ
            #        2: 合計 2匹
            #        3:25～30 cm
            #        4:0.8～1 kg
            columns = constants.ChokaHeaders
            df = pd.DataFrame(columns=columns)
            for row in chokaTable:
                values = {}
                htmlItems = row.find_all('td')
                if not htmlItems:
                    continue
                itemTexts = list(map(lambda x: x.text, htmlItems))
                itemTexts.pop(0)
                values['Species'] = itemTexts.pop(0)
                values['Count'] = Converter.getValues(itemTexts.pop(0))
                sizes = Converter.getRangeValues(itemTexts.pop(0))
                if sizes:
                    values['SizeMin'] = sizes[0]
                    values['SizeMax'] = sizes[1]
                weights = Converter.getRangeValues(itemTexts.pop(0))
                if weights:
                    values['WeightMin'] = weights[0]
                    values['WeightMax'] = weights[1]
                df = df.append(values, ignore_index=True)

            # 水温, 日付、コメントの抽出
            color = content.find(class_="color")
            waterTemp = Converter.getWaterTemp(color.text)
            chokaDate = Converter.getChokaDate(choka_head.text)
            df['Point'] = chokaPoint
            df['Date'] = chokaDate
            _logger.info("run : {},{}".format(chokaPoint, chokaDate))
            self.chokaData = self.chokaData.append(df)
            commentText = ''
            chokaComment = content.find(class_="choka_comment")
            if chokaComment:
                commentText = chokaComment.text
            commentDict = Converter.makeCommentDict(commentText)
            commentDict['WaterTemp'] = waterTemp
            commentDict['Date'] = chokaDate
            commentDict['Point'] = chokaPoint
            self.chokaComments = self.chokaComments.append(commentDict,
                                                           ignore_index=True)

    def run(self):
        """
        data ディレクトリ下の ダウンロード済みの釣果情報 html ファイルを順に読む。
        釣果情報を抽出して、CSV 形式にして保存する

        """
        template_dir = os.path.join(constants.DownloadDir)
        parseCount = 0
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                m = re.match('choka_(.+)_(\d+)\.html$', file)
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

import re
import os
import os.path
import logging
from dateutil import parser
import pandas as pd
from bs4 import BeautifulSoup
import piersfan.constants as constants
from piersfan.converter import Converter

Description='''
釣りビジョン釣果情報ホームページから釣果を取得する。取得情報は、
水温、コメント、魚種別釣果の3種
'''

class Parser():

    def __init__(self, point, year, month, page = 1):
        """
        魚種別釣果、コメントのデータフレームを初期化

        """
        self.chokaData = pd.DataFrame()
        self.chokaComments = pd.DataFrame(columns=constants.CommentHeaders)

    def parseHtml(self, htmlPath, chokaPoint, chokaPage):
        """
        釣果ホームページのファイルを読み込み、魚種別釣果、コメントのデータフレームに格納する

        """
        _logger = logging.getLogger(__name__)
        f = open(htmlPath)
        html = f.read()
        f.close()
        soup = BeautifulSoup(html, 'html.parser')
        chokaContents = soup.find_all(class_="choka_box")

        # 日別の釣果コンテンツを順に解析する
        for chokaContent in chokaContents:
            chokaInfo = chokaContent.find(class_="choka_info")
            chokaTable = chokaContent.find_all('tr')

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
                df= df.append(values, ignore_index=True)

            # 水温, 日付、コメントの抽出
            color = chokaContent.find(class_="color")
            waterTemp = Converter.getWaterTemp(color.text)
            chokaDate = Converter.getChokaDate(chokaInfo.text) 
            df['Point'] = chokaPoint
            df['Date'] = chokaDate
            _logger.info("run : {},{}".format(chokaPoint, chokaDate))
            self.chokaData = self.chokaData.append(df)
            commentText = ''
            chokaComment = chokaContent.find(class_="choka_comment")
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
                if  m:
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

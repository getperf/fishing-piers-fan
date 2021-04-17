import re
import time
import logging
import unicodedata
import piersfan.constants as constants
import datetime
import locale
from dateutil import parser

Description='''
釣りビジョンフィッシングピアース釣果情報ホームページから釣果を取得する。
HTML 要素を解析して変換する。
'''

class Converter():

    @staticmethod
    def getWaterTemp(str):
        # 【水温】13.5℃
        waterTemp = str.replace('\n', '').replace(' ', '')
        m = re.search(r'([0-9]+\.[0-9]+)', waterTemp)
        if m:
            return float(m.groups()[0])
        m = re.search('([0-9]+)', waterTemp)
        if m:
            return float(m.groups()[0])
        return None

    @staticmethod
    def getChokaDate(str):
        chokaDate = str.replace('\n', '').replace(' ', '')
        m = re.search('([0-9]+)年([0-9]+)月([0-9]+)日', chokaDate)
        if m:
            return parser.parse('/'.join(m.groups()))
        return None

    @staticmethod
    def getRangeValues(str):
        # 25～30 cm
        m = re.search(r'([0-9\.]+)～([0-9\.]+)\s*(cm|kg)', str)
        if m:
            vals = m.groups()
            return [float(vals[0]), float(vals[1])]

        # 39  cm
        m = re.search(r'([0-9\.]+)\s*(cm|kg)', str)
        if m:
            vals = m.groups()
            return [float(vals[0]), float(vals[0])]
        return None

    @staticmethod
    def getValues(str):
        m = re.search('([0-9]+)匹', str)
        if m:
            return float(m.groups()[0])
        if str:
            return str
        else:
            return None

    @staticmethod
    def get_header(comment, headers):
        m = re.search('(天気|水温|潮|入場者数)：(.*)', comment)
        if m:
            [item, value] = m.groups()
            if item == '天気':
                headers['Weather'] = value
            elif item == '潮':
                headers['Tide'] = value
            elif item == '水温':
                m2 = re.search(r'([0-9\.]+)℃', value)
                if m2:
                    vals = m2.groups()
                    headers['WaterTemp'] = float(vals[0])
            elif item == '入場者数':
                m2 = re.search(r'([0-9\.]+)名', value)
                if m2:
                    vals = m2.groups()
                    headers['Quantity'] = float(vals[0])

    @staticmethod
    def get_choka_table_value(comment, values):
        # comment = comment.strip()
        comment = unicodedata.normalize("NFKD", comment)
        m = re.search(r'合計 (\d+) 匹', comment)
        if m:
            values['Count'] = int(m.groups()[0])
            return

        # 25～30 cm
        m = re.search(r'([0-9\.]+)～([0-9\.]+)\s*(cm|kg)', comment)
        if m:
            [min_val, max_val, unit] = m.groups()
            if unit == 'cm':
                values['SizeMin'] = min_val
                values['SizeMax'] = max_val
            elif unit == 'kg':
                values['WeightMin'] = min_val
                values['WeightMax'] = max_val
            return

        # 39  cm
        m = re.search(r'([0-9\.]+)\s*(cm|kg)', comment)
        if m:
            [val, unit] = m.groups()
            if unit == 'cm':
                values['SizeMin'] = val
                values['SizeMax'] = val
            elif unit == 'kg':
                values['WeightMin'] = val
                values['WeightMax'] = val
            return
        return None


    @staticmethod
    def get_date(str):
        chokaDate = str.replace('\n', '').replace(' ', '')
        m = re.search('([0-9]+)年([0-9]+)月([0-9]+)日', chokaDate)
        if m:
            return parser.parse('/'.join(m.groups()))
        return None

    @staticmethod
    def makeCommentDict(comment):
        print("TEST")
        # commentDict = {'Comment': comment}
        commentDict = {'Comment': ''}
        # 入場者数:45人
        # 今日は強い風雨で釣りにくい中、コノシロ・イワシが一
        comment = comment.replace('\n', '').replace(' ', '')
        # m = re.search('入場者数:([0-9]+)人(.*)', comment)
        m = re.search('入場者数:([0-9]+?)人(.*)', comment)
        print(m.groups())
        if m:
            commentDict['Quantity'] = m.groups()[0]
            commentDict['Comment'] = m.groups()[1]
        return commentDict

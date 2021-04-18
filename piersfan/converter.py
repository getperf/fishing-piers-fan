import re
import time
import logging
import unicodedata
import piersfan.constants as constants
from datetime import datetime
import locale
from dateutil import parser

Description='''
釣りビジョンフィッシングピアース釣果情報ホームページから釣果を取得する。
HTML 要素を解析して変換する。
'''

class Converter():

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
    def get_comment(text, comments):
        """空白を整形し、削除する"""
        text = unicodedata.normalize("NFKD", text)
        text = text.replace('\n', '').replace(' ', '')
        comments['Comment'] = text
        m = re.search(r'\(.+?([0-9]+):([0-9]+)\)', text)
        if m:
            # comments['Time'] = m.groups()[0]
            # comments['Time'] = parser.parse(':'.join(m.groups()))
            time = datetime.strptime(':'.join(m.groups()),"%H:%M")
            date = comments['Date']
            comments['Time'] = datetime.combine(date.date(),time.time())

            # print(comments['Date'] + datetime.strptime(':'.join(m.groups()),"%H:%M"))
            # comments['Time'] = datetime.strptime(':'.join(m.groups()),"%H:%M")

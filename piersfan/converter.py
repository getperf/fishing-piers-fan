import logging
import re
import unicodedata
from datetime import datetime
from dateutil import parser

Description = '''
釣りビジョンフィッシングピアース釣果情報ホームページから釣果を取得する。
HTML 要素を解析して変換する。
'''

_logger = logging.getLogger(__name__)

class Converter:

    @staticmethod
    def get_header(comment, headers):
        m = re.search(r'(天気|水温|潮|入場者数)：(.*)', comment)
        if m:
            [item, value] = m.groups()
            if item == '天気':
                headers['Weather'] = value
            elif item == '潮':
                headers['Tide'] = value
            elif item == '水温':
                m2 = re.search(r'([0-9.]+)℃', value)
                if m2:
                    values = m2.groups()
                    headers['WaterTemp'] = float(values[0])
            elif item == '入場者数':
                m2 = re.search(r'([0-9.]+)名', value)
                if m2:
                    values = m2.groups()
                    headers['Quantity'] = float(values[0])

    @staticmethod
    def get_choka_table_value(comment, values):
        comment = unicodedata.normalize("NFKD", comment)
        m = re.search(r'合計 (\d+) 匹', comment)
        if m:
            values['Count'] = int(m.groups()[0])
            return

        # 25～30 cm
        m = re.search(r'([0-9.]+)～([0-9.]+)\s*(cm|kg)', comment)
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
        m = re.search(r'([0-9.]+)\s*(cm|kg)', comment)
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
    def get_date(comment):
        choka_date = comment.replace('\n', '').replace(' ', '')
        m = re.search('([0-9]+)年([0-9]+)月([0-9]+)日', choka_date)
        if m:
            return parser.parse('/'.join(m.groups()))
        return None

    @staticmethod
    def get_comment(text, comments):
        """空白を整形し、削除する"""
        text = unicodedata.normalize("NFKD", text)
        text = text.replace('\n', '')
        comments['Comment'] = text
        m = re.search(r'\(.+?([0-9]+):([0-9]+)\)', text)
        if m:
            time_label = ':'.join(m.groups())
            try:
                time = datetime.strptime(time_label, "%H:%M")
                date = comments['Date']
                comments['Time'] = datetime.combine(date.date(), time.time())
            except ValueError:
                _logger.warn("failed to parse time : {}".format(time_label))

import logging
import re
import unicodedata
from datetime import datetime
from dateutil import parser

Description = '''
フィッシングピアース釣果情報ホームページから釣果を取得する。
HTML 要素を解析して変換する。
'''

_logger = logging.getLogger(__name__)

class Converter:

    @staticmethod
    def get_header(comment, headers):
        """
        HTMLヘッダーから天気などを抽出し、辞書に登録します
        """
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
        """
        HTML 釣果テーブルから各セル値を抽出し、辞書に登録します
        """
        comment = unicodedata.normalize("NFC", comment)
        m = re.search(r'合計\s*(\d+)\s*匹', comment)
        if m:
            values['Count'] = int(m.groups()[0])
            return

        # 最大、最小魚種サイズの抽出。25～30 cm
        m = re.search(r'([0-9.]+)\s*-\s*([0-9.]+)\s*(cm|kg)', comment)
        if m:
            [min_val, max_val, unit] = m.groups()
            if unit == 'cm':
                values['SizeMin'] = float(min_val)
                values['SizeMax'] = float(max_val)
            elif unit == 'kg':
                values['WeightMin'] = float(min_val)
                values['WeightMax'] = float(max_val)
            return

        # 単一の魚種サイズの抽出。39  cm
        m = re.search(r'([0-9.]+)\s*(cm|kg)', comment)
        if m:
            [val, unit] = m.groups()
            if unit == 'cm':
                values['SizeMin'] = float(val)
                values['SizeMax'] = float(val)
            elif unit == 'kg':
                values['WeightMin'] = float(val)
                values['WeightMax'] = float(val)
            return
        return None

    @staticmethod
    def get_date(comment):
        """
        日付文字列を解析して、datetime 型で返します
        """
        choka_date = comment.replace('\n', '').replace(' ', '')
        m = re.search('([0-9]+)年([0-9]+)月([0-9]+)日', choka_date)
        if m:
            return parser.parse('/'.join(m.groups()))
        return None

    @staticmethod
    def get_comment(text, comments):
        """
        HTML コメントから、コメントと時刻を抽出し、辞書に登録します
        """
        """空白を整形し、削除する"""
        text = unicodedata.normalize("NFC", text)
        text = text.replace('\n', '')
        comments['Comment'] = text
        m = re.search(r'[\(（].+?([0-9]+):([0-9]+)[\)）]', text)
        if m:
            time_label = ':'.join(m.groups())
            date = comments['Date']

            """コメント内の時刻取得で、「4/197:05」など空白が不足している
            時に時刻解析エラーとなる。この場合は 0:00でセットする"""
            try:
                time = datetime.strptime(time_label, "%H:%M")
                comments['Time'] = datetime.combine(date.date(), time.time())
            except ValueError:
                comments['Time'] = date
                _logger.warning("parse time failed : {}".format(time_label))
        else:
            comments['Time'] = comments['Date']

    @staticmethod
    def clensing_summary_comment(comment):
        """
        釣果サマリコメントから不要な文を取り除く
        """

        """箇条書きで始まる箇所からそれ以降の文は除く"""
        comment = unicodedata.normalize("NFC", comment)
        lines = re.split(r'[【■★※＊]', comment)
        if lines:
            comment = lines[0]

        """定型文は除く"""
        lines = re.split(r'[。\n]', comment)
        comment2 = ''
        for line in lines:
            if len(line) == 0:
                continue
            if re.search(r'本日(.+)ご来場', line):
                # print("HIT1")
                continue
            elif re.search(r'(お待ちして|What\'sNew|カード|提示|事前予約|急激に暗く|駐車)', line):
                continue
            else:
                comment2 += line + "。"
        if len(comment2) > 0:
            comment = comment2
        return comment

    @staticmethod
    def clensing_newsline_comment(comment):
        """
        釣果サマリコメントから不要な文を取り除く
        """
        comment = unicodedata.normalize("NFC", comment)
        lines = re.split(r'[【■★※＊]', comment)
        if lines:
            comment = lines[0]

        """定型文は除く"""
        lines = re.split(r'[。\n]', comment)
        comment2 = ''
        for line in lines:
            if len(line) == 0:
                continue
            if re.search(r'本日(.+)ご来場', line):
                # print("HIT1")
                continue
            elif re.search(r'(おはよう|交通|営業時間|ご来場|急激に暗く|カード|駐車|予約|受付|入場)', line):
                continue
            else:
                comment2 += line + "。"
        if len(comment2) > 0:
            comment = comment2

        return comment
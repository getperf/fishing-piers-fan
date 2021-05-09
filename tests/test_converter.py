import re
import datetime

from piersfan.config import Config
from piersfan.converter import Converter


# py.test tests/test_converter.py -v --capture=no -k test_get_biz_day

def test_get_header():
    headers = dict()
    Converter.get_header("天気：曇り時々雨", headers)
    assert headers['Weather'] == "曇り時々雨"
    Converter.get_header("水温：16.3℃", headers)
    assert headers['WaterTemp'] == 16.3
    Converter.get_header("潮：大潮", headers)
    assert headers['Tide'] == "大潮"
    Converter.get_header("入場者数：104名", headers)
    assert headers['Quantity'] == 104
    print(headers)

def test_get_cell_value():
    values = dict()
    Converter.get_choka_table_value("25 - 28 cm", values)
    assert values == {'SizeMin': 25, 'SizeMax': 28}

    values2 = dict()
    Converter.get_choka_table_value("合計24匹", values2)
    assert values2 == {'Count': 24}

    values3 = dict()
    Converter.get_choka_table_value("1.90-2.50kg", values3)
    assert values3 == {'WeightMin': 1.9, 'WeightMax': 2.5}



def test_get_date():
    assert Converter.get_date("2021年04月13日[火]天気") == datetime.datetime(2021, 4, 13, 0, 0)
    assert Converter.get_date("2021年04月12日[月]") == datetime.datetime(2021, 4, 12, 0, 0)


def test_get_comment():
    comments = dict(Date=datetime.datetime(2021, 4, 12, 0, 0))
    Converter.get_comment("""※各釣果写真はクリックすると大きく表示されます。

東桟橋の浮きフカセでクロダイが出ています。
現在南風が少し強くなって来ています。
(磯子12:04)""", comments)
    assert comments['Time'] == datetime.datetime(2021, 4, 12, 12, 4)

def test_get_comment_time_error():
    comments = dict(Date=datetime.datetime(2021, 4, 12, 0, 0))
    Converter.get_comment("""(磯子4/1912:04)""", comments)
    assert comments['Time'] == datetime.datetime(2021, 4, 12, 0, 0)

def test_get_comment_nfd():
    comments = dict(Date=datetime.datetime(2021, 4, 12, 0, 0))
    str = "アジ、イワシ、ウミタナゴ、カサゴ、コノシロ、メバル"
    Converter.get_comment(str, comments)
    assert comments['Comment'] == "アジ、イワシ、ウミタナゴ、カサゴ、コノシロ、メバル"

def test_cleansing_comment():
    comment_path = Config.test_resource("comment1.txt")
    f = open(comment_path)
    comment = f.read()
    f.close()
    comment = Converter.clensing_summary_comment(comment)
    assert comment
    print(comment)

    comment_path = Config.test_resource("comment2.txt")
    f = open(comment_path)
    comment = f.read()
    f.close()
    comment2 = Converter.clensing_summary_comment(comment)
    assert comment2
    print(comment2)

def test_get_biz_day():
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 1, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 2, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 3, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 4, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 5, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 6, 0, 0)) == "WeekDay"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 7, 0, 0)) == "WeekDay"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 8, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 9, 0, 0)) == "Holiday"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 10, 0, 0)) == "WeekDay"
    assert Converter.get_biz_day(datetime.datetime(2021, 5, 11, 0, 0)) == "WeekDay"

def test_cleansing_weather():
    assert Converter.cleansing_weather('曇り') == "曇"
    assert Converter.cleansing_weather('晴れ') == "晴"
    assert Converter.cleansing_weather('晴れのち曇り') == "晴れのち曇り"


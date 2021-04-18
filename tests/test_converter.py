import datetime

from piersfan.converter import Converter


# py.test tests/test_converter.py -v --capture=no -k test_get_header

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

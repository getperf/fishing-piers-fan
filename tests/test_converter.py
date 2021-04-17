import re
import sys
import os
import pytest
import datetime
import pandas as pd
# from piersfan.parser import Parser
import piersfan
from piersfan import converter
from piersfan.converter import Converter

# py.test tests/test_converter.py -v  -k test_makeCommentDict
# py.test tests/test_converter.py -v  -k test_get_header
# py.test tests/test_converter.py -v --capture=no -k test_get_date

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

def test_getWaterTemp():
    assert Converter.getWaterTemp("【水温】14℃") == 14.0
    assert Converter.getWaterTemp("【水温】15.3℃") == 15.3
    assert Converter.getWaterTemp("【水温】") == None

def test_getChokaDate():
    assert Converter.getChokaDate("2021年4月2日( )") == datetime.datetime(2021, 4, 2, 0, 0)

def test_convertValue():
    assert Converter.getValues("合計 13匹") == 13.0
    assert Converter.getRangeValues("25～30 cm") == [25, 30]
    assert Converter.getRangeValues("0.8～1.4 kg") == [0.8, 1.4]
    assert Converter.getValues("") == None

def test_makeCommentDict():
    print("TEST")
    assert Converter.makeCommentDict("入場者数:154人test") == {'Comment': 'test', 'Quantity': '154'}
    assert Converter.makeCommentDict("入場者数:154人") == {'Quantity': '154'}

import re
import sys
import os
import pytest
import datetime
import pandas as pd
import pkg_resources
from importlib.resources import read_text
import importlib
from piersfan.parser import Parser

# py.test tests/test_parser.py -v --capture=no -k test_not_found

def get_test_data(filename):
    return pkg_resources.resource_filename("tests.resources", filename)

def test_not_found():
    # test_file = open(
    #     pkg_resources.resource_filename('tests.resources','not_found1.html'),'r')
    # for line in test_file:
    #     print(line)
    # print(pkg_resources.resource_filename('tests.resources','not_found1.html'))
    # print(read_text("lib2to3", "Grammar.txt"))
    # print(read_text("piersfan", "aaa", "Grammar.txt"))
    print(">>>End of File")
    print(importlib.util.resolve_name("lib2to3", "Grammar.txt"))
    print(pkg_resources.resource_filename("piersfan", "not_found1.html"))
    print(pkg_resources.resource_filename("tests.resources", "not_found1.html"))
    not_found_html = get_test_data("not_found1.html")
    contents = Parser
    # parser = Parser()
    # assert parser.getWaterTemp("【水温】14℃") == 14.0
    # assert parser.getWaterTemp("【水温】15.3℃") == 15.3
    # assert parser.getWaterTemp("【水温】") == None

def test_getChokaDate():
    parser = Parser()
    assert parser.getChokaDate("2021年4月2日( )") == datetime.datetime(2021, 4, 2, 0, 0)

def test_convertValue():
    parser = Parser()
    assert parser.convertValue("合計 13匹") == 13.0
    assert parser.convertValue("25～30 cm") == [25, 30]



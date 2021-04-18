from piersfan.parser import Parser
from piersfan.config import Config


# py.test tests/test_parser.py -v --capture=no -k test_parse_all

def test_not_found():
    html_path = Config.test_resource("not_found1.html")
    assert not Parser("daikoku").parse_html(html_path)


def test_daikoku_html_parseer():
    html_path = Config.test_resource("daikoku1.html")
    parser = Parser("daikoku").parse_html(html_path)
    timestamps = parser.get_timestamps()
    print(parser.choka.columns)
    print(parser.comment.columns)
    print(parser.newsline.columns)
    assert timestamps['choka']
    assert timestamps['newsline']


def test_daikoku_only_newsline_parser():
    html_path = Config.test_resource("daikoku1_newsline.html")
    parser = Parser("daikoku").parse_html(html_path)
    timestamps = parser.get_timestamps()
    assert not timestamps['choka']
    assert timestamps['newsline']


def test_isogo_html_parseer():
    html_path = Config.test_resource("isogo1.html")
    parser = Parser("isogo").parse_html(html_path)
    timestamps = parser.get_timestamps()
    print(timestamps)
    assert timestamps['choka']
    assert timestamps['newsline']


def test_honmoku_html_parseer():
    html_path = Config.test_resource("honmoku1.html")
    parser = Parser("honmoku").parse_html(html_path)
    timestamps = parser.get_timestamps()
    print(timestamps)
    assert timestamps['choka']
    assert timestamps['newsline']


def test_export():
    html_path = Config.test_resource("daikoku1.html")
    parser = Parser("daikoku").parse_html(html_path)
    parser.export('csv')


def test_append():
    html_path = Config.test_resource("daikoku1.html")
    parser = Parser("daikoku").parse_html(html_path)
    html_path2 = Config.test_resource("isogo1.html")
    parser2 = Parser("isogo").parse_html(html_path2)
    parser.append(parser2)
    timestamps = parser.get_timestamps()
    print(timestamps)
    assert timestamps['choka']
    assert timestamps['newsline']


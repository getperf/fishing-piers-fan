# 横浜フィッシングピアース釣果リサーチ

横浜フィッシングピアースのホームページにアクセスし、釣果情報を取得して
SQLite3 データベースに保存します。

* 横浜フィッシングピアースの釣果ページのダウンロード、値の抽出、データベース
  へのロードをします
* ロードしたデータベースは、Jupyter notebook を用いて分析をします
* 定期的に実行することで、差分をロードします

## インストール



## 使用方法

## 釣果情報の分析


* URLで釣り場を指定
* 気温、当日の状況コメント、魚種別釣果の3種類を保存する
* 日付をキーにする
* 結果は CSV に保存

モジュール構成
--------------

* html ダウンロード、施設ディレクトリ、ページ舞ファイル
* テキストパース
* SQLite3 保存

インストール
------------


使用方法
--------






横浜釣果情報検索
================

cd /c/home/hugo/choka

python -m venv .

pip install beautifulsoup4

C:\home\hugo\choka

要件検討
-------

横浜フィッシングピアースの釣果情報ホームページにアクセスし、
指定した釣り場の釣果情報を取得する

* URLで釣り場を指定
* 気温、当日の状況コメント、魚種別釣果の3種類を保存する
* 日付をキーにする
* 結果は CSV に保存

モジュール構成
--------------

* html ダウンロード、施設ディレクトリ、ページ舞ファイル
* テキストパース
* SQLite3 保存

使用方法
-------

from choka.util import scraper

choka = scraper.get("https://www.fishing-v.jp/choka/choka_detail.php?s=11285")
print(choka.temp)
print(choka.comment)
print(choka.results)

setup.py 準備
--------------

https://qiita.com/Tadahiro_Yamamura/items/2cbcd272a96bb3761cc8


# Installation

Simply run:

    python -m pip install -e .

# 開発環境のインストール

    python -m pip install --force-reinstall --editable .

# Usage

To use it:

    gcbat --help

HTMLダウンロード
-----------------

大黒

全880件 2018/4/12 ～ 2021/3/30

https://www.fishing-v.jp/choka/choka_detail.php?s=11285&pageID=1
https://www.fishing-v.jp/choka/choka_detail.php?s=11285&pageID=88

磯子

全963件 2018/3/31 ～ 2021/3/30

https://www.fishing-v.jp/choka/choka_detail.php?s=11286&pageID=1
https://www.fishing-v.jp/choka/choka_detail.php?s=11286&pageID=97

本牧

全587件

https://www.fishing-v.jp/choka/choka_detail.php?s=11284&pageID=1
https://www.fishing-v.jp/choka/choka_detail.php?s=11284&pageID=58

dataframe から、json に変換

mkdir data
cd data
wget https://www.fishing-v.jp/choka/choka_detail.php?s=11285&pageID=1

施設ごとに順に巡回する
何カ月前からダウンロードするかを指定
URL フォームデータに年、月を指定し、開始月から順にアクセス
各ページをダウンロード
    ページの解析結果で 「データがありません」がでたら、翌月にカウントアップ
    最終更新日付を記録する
    巡回して取得したページの日付が前回の最終更新日付よりも古ければ終了する

残件整理

ダウンロード
    釣果ページの日付のチェック、取得日付が前回実行日付よりも古い場合は何もしない ⇒保留
解析
    download ディレクトリ下の HTML ファイルをスキャンして解析、csv 保存

download ディレクトリ下の HTML ファイルをスキャン

ファイル整形、コメント追加、Readme 作成

jupyter report 連携
sqlalchemy db 接続

piersfan save

sqlite3 data/fishing_result.sqlite3

select count(*) from fishing_newslines;
75338
select count(*) from fishing_results;
81804
select count(*) from fishing_comments;
4879

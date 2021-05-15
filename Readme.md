# Fishing Piers Fan

横浜海釣り施設釣行計画のための釣果分析プロジェクト。

横浜フィッシングピアーズホームページから釣果情報を抽出してデータベースを作成します。
データベースを分析することで釣行計画に利用します。

![アジ分析例](docs/sample_report1.png)

釣果分析のブログ記事があります。

https://mon3nr.github.io/blog1/

## インストール

Python 3.9 の環境が必要です。

pip install でインストールします。

```
cd {インストール先}/fishing-piers-fan
python -m pip install -e .
```

開発環境なら --force-reinstall を追加してください。

```
python -m pip install --force-reinstall -e .
```

## 使用方法

*yfp --init* コマンドを使用して、データベースを初期化します。

```
yfp --init
```

釣果データの抽出・ロードを実行します。既定の設定だと、当月分のホームページからデータを抽出してロードします。

```
yfp
```

--page {値} で直近のページから何ページ目までをダウンロードするかを指定します。
データベースへのロードは、更新があった差分データのみマージしてロードします。

```
# 直近の10ページまでを取得してロード
yfp --page 10  
```

--month オプションで何カ月前からのページから巡回するかを指定します。

```
# 過去3年分の取得とロード
yfp --month 36 
```

> **注意事項**
>
>  横浜フィッシングピアーズの1年分の釣果ページ数は数千ページになります。
--month オプションで長期間のダウンロードをする場合は、
夜間に実行する、巡回インターバルを長くするなど、サイトへの負荷影響を意識して実行してください。

--show オプションでデータベースファイルなどのディレクトリ構成情報を出力します。

```
yfp --show
```

後述の jupyter notebook でのデータ分析では、本コマンドで表示された、データベースファイルパスを指定します。

これらの設定は、 **{project_dir}/data/config.toml** に記述します。

## 分析チュートリアル

**notebook** ディレクトリ下に jupyter notebook のサンプルレポートがあるので、本レポートを開いて利用方法を確認してください。

jupyter notebook を起動します。

```
cd {インストール先}/fishing-piers-fan
jupyter notebook
```

Web ブラウザが起動され、Jupyter notebook のホームページが表示されます。

>  **注意事項**
>
> Linux 環境の場合は、ログメッセージに出力された URL を Web ブラウザに入力してください。

リストからディレクトリ **notebook** を選択し、
 **sample1.ipynb** を開きます。

Juptyer notebook とのインターフェースは、ロードした 
SQLite3 データベースのみになります。SQLite3 データベースのパスを確認する場合は以下を実行してください。

```
from piersfan.config import Config
print(Config.get_db_path())
```

表示された SQLite3 データベースパスを指定して、データベースに接続します。

```
conn = sqlite3.connect("{SQLite3データベースパス}")
```

## データベースモデル

データベースの主要なテーブルは以下の３つのテーブルとなります。
SQL を用いてこれらテーブルを検索します。

  ![ER図](docs/erd.drawio.png)

各テーブル定義は以下の通りです。

### fishing_results (魚種別釣果)

その日の魚種別釣果を記録します。

* キー : 
    * Date(日付), Point(施設名), Species(魚種)

* カラム : 
    * Count(釣果数), SizeMin(最小cm), SizeMax(最大cm),WeightMin(最小kg), WieghtMax(最大kg), Comment(コメント), Place(場所)

### fishing_comments (釣果サマリ)

その日の釣果コメント、入場者数、水温などのサマリ情報を記録します。

* キー : 
    * Date(日付), Point(施設名)

* カラム : 
    * Weather(天気), WaterTemp(水温℃), Quantity(入場者数), Comment(コメント), Tide(潮), Time(時刻)

### fishing_newslines (釣果記事)

釣果速報のコメントを記録します。

* キー : 
    * Date(日付), Time(時刻), Point(施設名)

* カラム : 
    * Comment(コメント), Weather(天気)

## PowerBI によるデータ分析

Miscrosoft 製 PowerBI を用いて釣果データベースの分析を行います。

* セットアップ手順； [PowerBIセットアップ](./docs/setup_powerbi.md)
* 利用手順 ブログ；[横浜フィッシングピアーズ海釣り施設、釣果分析2](https://mon3nr.github.io/blog1/blog/yfpreserch02/)

## 注意事項

横浜フィッシングピアーズホームページデータの二次利用について、動画、画像を除くテキスト情報の利用は特に規定はなく、
一般的な常識の範囲内での利用は問題ないとの回答がありました。
ただし、ブログなどに掲載する場合は事前申請が必要になります。詳細は以下URLを参照してください。

http://daikoku.yokohama-fishingpiers.jp/use.php

> 施設内で撮影（写真・動画）を行なう際には、事前に施設に許可申請が必要です。
SNSへ動画や記事を掲載する場合も、同様に事前のお申込みをお願い致します。
また、撮影内容につきましては、当施設のルールとマナーをお守りください。

## Refference

1. [横浜フィッシングピアーズ](http://daikoku.yokohama-fishingpiers.jp/index.php)
2. [自転車散歩、釣り記録](https://mon3nr.github.io/blog1/)

## COPYRIGHT

Copyright 2021, Minoru Furusawa <mon3nr@gmail.com>

## LICENSE

This program is released under [GNU General Public License, version 2](http://www.gnu.org/licenses/gpl-2.0.html) or later.


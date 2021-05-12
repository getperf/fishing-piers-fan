# PowerBIセットアップ

Microsoft 製 PowerBI を用いて fishing-piers-fan の釣果データベースを分析します。

## 事前準備

* Windows 10 64bit 環境が必要です。
* PowerBI の SQLlite3 接続用に、SQLite3 ODBC ドライバーのインストールが必要です。

## SQLite3 ODBC ドライバーインストール

以下のSQLite3 ODBC ドライバーダウンロードサイトにアクセスします。

```
http://www.ch-werner.de/sqliteodbc
```

以下の記述のCurrent version のリストから、
以下の32ビット板、64ビット版の両方をダウンロード

```
Current version
sqliteodbc.exe     # 32bit版
sqliteodbc_w64.exe # 64bit版
```

PowerBIは 64 bit 版 ODBC ドライバを使用しますが、
ODBC の設定には 32bit 版 ODBC が必要なので、32bit, 64bit の
両バージョンをインストールします。

ダウンロードしたインストールファイルをそれぞれ起動し、
既定の設定のままインストールを実行します。

## ODBC 接続設定

インストールが終わったら以下のコマンドを起動します。

```
C:\Windows\SysWOW64\odbcad32.exe
```

ユーザ DNSから追加をクリックし、セットアップするドライバーリストから、SQLite3 ODBC Driver を選択します。

Data Source Name に fishing_result を入力して、OK をクリックします。

設定はこれで終了です。Data Source Name 以外の設定は不要です。

## PowerBI インストール

以下の PowerBI ダウンロードサイトにアクセスします。

```
https://powerbi.microsoft.com/ja-jp/downloads/
```

Mycrosoft Power BI Desktop から、高度なダウンロードオプションを選択します。

日本語を選択して、ダウンロードをクリックします。

PBIDesktopSetup_x64.exe を選択して、ダウンロードします。

ダウンロードしたファイル PBIDesktopSetup_x64.exe を実行します。

既定の設定のままインストールを行い、インストールを完了します。

## PowerBI の起動

Windows スタートメニューから、Microsft Power BI Desktop を起動します。

他のレポートを開くを選択し、以下のパスの釣果情報分析レポートファイルを開きます。

```
{fishing_piers_fanホーム}/notebook/yfpresearch1.pbix
```

## PowerBI DB接続設定(初回のみ必要)

PowerBI のメニューから、ファイル、オプションと機能の設定、データソース設定を選択します。

データソースの設定をクリックします。

ソースの変更をクリックします。

データソース名(DNS)に fishing_result を選択します。

詳細設定オプションの接続文字列に以下の記述で、SQLite3 fishing_result.db のパスを指定します。


```
database={fishing_piers_fanホーム}/data/fishing_result.db
```

サポートされている行の削減句に LIMIT を選択します。

OK ボタンをクリックして、設定を完了します。

PowerBI画面から、「適用されていない保留中の変更がクエリにあります。」のメッセージが表示され、変更の適用をクリックします。

ログイン画面が表示され、ユーザー名に任意の名前 test を入力して接続します。

PowerBI のメニューから、ファイル、保存を選択し、設定を保存します。

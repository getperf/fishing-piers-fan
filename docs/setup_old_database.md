## 旧データベース復元手順

本手順では、2025年2月のサイト刷新以前に取得された釣果データを復元する方法を説明します。\
復元後は、最新の釣果データを再度取得することで、現在のデータベースを補完できます。\
PowerShell 環境での作業を前提としています。

***

## 手順

### ✅ 前提条件

- 本プロジェクトがインストール済みであること

- `sqlite3` ユーティリティが使用可能であること（パスが通っていること）

### 1. データディレクトリへ移動

```shell
cd {プロジェクトホームディレクトリ}\data
```

### 2. データベースのバックアップ作成

```shell
copy fishing_result.db fishing_result.db_bakup
```

### 3. 旧データベースのリストア

```shell
cmd /c "sqlite3 dump.db < fishing_result_20250131.sql"
```

### 4. データベースを差し替え

```shell
copy dump.db fishing_result.db
```

### 5. 最新データの再ロード（2025年1月31日以降のデータ）

2025年1月31日から本日までの日数を `--day` に指定して、最新データを取得します。

powershell

コピーする編集する

```shell
yfp -q --day 90  # 例：90日分を取得 yfp -d
yfp -d # データベースロード
```

※ 実行日によって `--day` の値を調整してください。

### 6. Power BI で復元を確認

Power BI を起動し、釣果データが正しく復元・更新されていることを確認してください。

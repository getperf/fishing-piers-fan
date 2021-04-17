# フィッシングTV釣果情報ホームページURL

UrlFishingPiers = "https://www.fishing-v.jp/choka/choka_detail.php?s={}&pageID={}"

# HTMLダウンロードファイル保存場所

DownloadDir = 'data'

# 釣果情報を保存するデータベースファイル名

ChokaDB = 'choka_db.sqlite3'

# 魚種別釣果カラム

header_choka = ['Date', 'Point', 'Species', 'Count', 'SizeMin', 'SizeMax', 'WeightMin', 'WeightMax', 'Comment', 'Place']

# コメントカラム

header_comment = ['Date', 'Point', 'Weather', 'WaterTemp', 'Quantity', 'Comment']

# ニュースラインカラム

header_newsline = ['Date', 'Point', 'Comment']

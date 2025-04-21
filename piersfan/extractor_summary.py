import logging
import pandas as pd

from piersfan.config import Config
from piersfan.converter import Converter
from piersfan.extractor import Extractor

Description = """
フィッシングピアースサイトから釣果情報を取得する
"""

_logger = logging.getLogger(__name__)

# クエリ部分
FISH_FIELDS = "\n".join(
    f"""      fish{i}Name
      fish{i}MinSize
      fish{i}MaxSize
      fish{i}Unit
      fish{i}Count
      fish{i}Place""" for i in range(1, 31)
)

# MiddlePostsByFacilityAndDate
QUERY = f"""
query LastPostsByFacilityAndDate(
  $facility: String!
  $date: ModelStringKeyConditionInput
  $sortDirection: ModelSortDirection
  $limit: Int
  $nextToken: String
) {{
  lastPostsByFacilityAndDate(
    facility: $facility
    date: $date
    sortDirection: $sortDirection
    limit: $limit
    nextToken: $nextToken
  ) {{
    items {{
      id
      date
      month
      facility
      sentence
      weather
      waterTemp
      tide
      visitors
{FISH_FIELDS}
      images
      createdAt
      updatedAt
      __typename
    }}
    nextToken
    __typename
  }}
}}
""".strip()


class ExtractorSummary:
    def __init__(self, extractor : Extractor):
        self.extractor = extractor

    def fetch_posts(self, facility, filter_date):
        all_items = []
        next_token = None

        while True:
            variables = {
                "facility": facility,
                "date": {"ge": filter_date},
                "sortDirection": "DESC",
                "limit": 100,
                "nextToken": next_token,
            }

            payload = {"query": QUERY, "variables": variables}
            response = self.extractor.fetch_data(payload)
            data = response["data"]["lastPostsByFacilityAndDate"]
            items = data["items"]
            all_items.extend(items)
            # print(f"Fetched {len(items)} items, nextToken={next_token}")

            next_token = data.get("nextToken")
            if not next_token:
                break

        return all_items

    def save_to_summary_csv(self, items, facility):
        df = pd.DataFrame(items)
        df.drop(columns=["__typename"], errors='ignore', inplace=True)
        df.rename(columns={
            "date": "Date", "facility": "Point", "weather": "Weather", 
            "waterTemp": "WaterTemp", "visitors": "Quantity", 
            "sentence": "Comment", "tide": "Tide"
        }, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.date
        df["Summary"] = df["Comment"].apply(Converter.clensing_summary_comment)
        df["BizDay"] = df["Date"].apply(Converter.get_biz_day)
        df = df[["Date", "Point", "Weather", "WaterTemp", "Quantity", "Comment", "Tide", "Summary", "BizDay"]]

        output_file = Config.get_csv_path("comment", facility)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        _logger.info(f"Saved {len(df)} records to {output_file}")

    def save_to_result_csv(self, items, facility):
        fish_rows = []

        for item in items:
            date = item.get("date")
            point = item.get("facility")

            for i in range(1, 30):
                name = item.get(f"fish{i}Name")
                if not name:
                    continue  # 魚種名がない場合はスキップ

                unit = item.get(f"fish{i}Unit")
                min_val = item.get(f"fish{i}MinSize")
                max_val = item.get(f"fish{i}MaxSize")
                count = item.get(f"fish{i}Count")
                place = item.get(f"fish{i}Place")

                # サイズ or 重量の割り当て
                size_min = size_max = weight_min = weight_max = None
                if unit == "cm":
                    size_min = min_val
                    size_max = max_val
                else:
                    weight_min = min_val
                    weight_max = max_val

                fish_rows.append({
                    "Date": date,
                    "Point": point,
                    "Species": name,
                    "Count": count,
                    "SizeMin": size_min,
                    "SizeMax": size_max,
                    "WeightMin": weight_min,
                    "WeightMax": weight_max,
                    "Place": place
                })

        df = pd.DataFrame(fish_rows)
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.date

        # CSV出力
        output_file = Config.get_csv_path("choka", facility)
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        _logger.info(f"Saved {len(df)} choka records to {output_file}")

    def run(self, facility, filter_date):
        _logger.info(f"Fetching summary posts for facility={facility}, date>={filter_date}")
        items = self.fetch_posts(facility, filter_date)
        if not items:
            _logger.info(f"No data found for facility={facility}, date>={filter_date}")
            return
        self.save_to_summary_csv(items, facility)
        self.save_to_result_csv(items, facility)

import csv
import logging
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import requests

from piersfan.config import Config
from piersfan.converter import Converter
from piersfan.extractor import Extractor

Description = """
フィッシングピアースサイトから釣果情報を取得する
"""

_logger = logging.getLogger(__name__)

QUERY = """
query MiddlePostsByFacilityAndDate(
  $facility: String!
  $date: ModelStringKeyConditionInput
  $sortDirection: ModelSortDirection
  $filter: ModelMiddlePostFilterInput
  $limit: Int
  $nextToken: String
) {
  middlePostsByFacilityAndDate(
    facility: $facility
    date: $date
    sortDirection: $sortDirection
    filter: $filter
    limit: $limit
    nextToken: $nextToken
  ) {
    items {
      date
      time
      facility
      sentence
      __typename
    }
    nextToken
    __typename
  }
}
"""

class ExtractorNewsLine:
    def __init__(self, extractor : Extractor):
        self.extractor = extractor

    def fetch_posts(self, facility, date_ge):
        all_items = []
        next_token = None

        while True:
            variables = {
                "facility": facility,
                "date": {"ge": date_ge},
                "sortDirection": "DESC",
                "limit": 100,
                "nextToken": next_token,
            }

            payload = {"query": QUERY, "variables": variables}
            response = self.extractor.fetch_data(payload)
            data = response["data"]["middlePostsByFacilityAndDate"]
            items = data["items"]
            all_items.extend(items)

            next_token = data.get("nextToken")
            if not next_token:
                break

        return all_items

    def save_to_csv(self, items, facility):
        df = pd.DataFrame(items)
        df.drop(columns=["__typename"], errors='ignore', inplace=True)
        df.rename(columns={
            "date": "Date", "time": "Time", "facility": "Point", "sentence": "Comment"
        }, inplace=True)
        df["Comment"] = df["Comment"].apply(Converter.clensing_newsline_comment)
        df.dropna(subset=["Comment"], inplace=True)
        output_file = Config.get_csv_path("newsline", facility)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        _logger.info(f"Saved {len(df)} records to {output_file}")

    def run(self, facility, date):
        _logger.info(f"Fetching newsline posts for facility={facility}, date>={date}")
        items = self.fetch_posts(facility, date)
        if not items:
            _logger.info(f"No newsline posts found for facility={facility}, date>={date}")
            return
        self.save_to_csv(items, facility)

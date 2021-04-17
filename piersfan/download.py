import time
import requests
import logging
import argparse
from bs4 import BeautifulSoup
import csv
import pandas as pd
import toml
import urllib
import os.path

Description='''
横浜フィッシングピアースの釣果情報ホームページをダウンロードする
'''

UrlFishingPiers = "http://{}.yokohama-fishingpiers.jp/choka.php"
CrawlInterval = 5
DownloadDir = 'data'

class Download():

    def loadConfig(self, configFile='config.toml'):
        self.choka = toml.load(configFile)
        # logger.info("read {}".format(DeviceConfig))
        print("area load : {}".format(self.choka))
        return self

    def getUrl(self, name):
        return UrlFishingPiers.format(name)

    def getFormData(self, year, month, page = 1):
        return 'page={}&choko_ys={}&choko_ms={:0=2}'.format(page, year, month)

    def getDownloadFile(self, name, year, month, page = 1):
        return 'choka_{}_{}_{:0=2}_{:0=3}.html'.format(name, year, month, page)

    def download(self, areaName, year, month, page = 1):
        downloadUrl = self.getUrl(areaName)
        formData = self.getFormData(year, month, page)
        downloadFile = self.getDownloadFile(areaName, year, month, page)
        savePath = os.path.join(DownloadDir, downloadFile)
        # data = urllib.request.urlopen(downloadUrl).read()
        values = {'page': '1', 'choko_ys': '2021', 'choko_ms':'04'}
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii') # data should be bytes
        req = urllib.request.Request(downloadUrl, data)
        data = urllib.request.urlopen(req).read()
        with open(savePath, mode="wb") as f:
            f.write(data)
        print("download area:{}, date:{}/{}, page:{}".format(areaName, year, month, page))

    def run(self):
        for area in self.choka['area']:
            areaName = area['name']
            areaId = area['id']
            lastPage = area['last_page']
            for page in range(1, lastPage):
                self.download(areaName, areaId, page)
                time.sleep(CrawlInterval)

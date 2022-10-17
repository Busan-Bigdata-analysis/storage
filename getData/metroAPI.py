import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
import pymysql
import requests

# 변수 관리
Servicekey = '{api key}'
STATION_CODE = pd.read_excel('getData/data/역 코드목록.xlsx',skiprows=1)


def get_api(scode):
    url = 'http://data.humetro.busan.kr/voc/api/open_api_distance.tnn'
    params ={'serviceKey' : Servicekey, 'act' : 'json', 'scode' : scode }

    response = requests.get(url,params=params)
    response.raise_for_status()
    response.encoding='EUC-KR'

    api = response.text
    stationAPI = json.loads(api)

    return(stationAPI)
    pass

def main():
    print(get_api(101))
    pass

if __name__=='__main__':
    main()
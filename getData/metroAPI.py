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
Servicekey = 'api key'
STATION_CODE = pd.read_excel('getData/data/역 코드목록.xlsx',skiprows=1)


def get_api(scode):
    url = 'http://data.humetro.busan.kr/voc/api/open_api_distance.tnn'
    params ={'serviceKey' : Servicekey, 'act' : 'json', 'scode' : scode }

    response = requests.get(url,params=params)
    response.raise_for_status()
    response.encoding='EUC-KR'

    api = response.text
    stationAPI = json.loads(api)

    return stationAPI
    pass

def get_tuple(scode):
    json_data = get_api(scode)
    station_name = json_data['response']['body']['item'][0]['startSn']
    lowwer_stopping_time = json_data['response']['body']['item'][0]['stoppingTime']
    if len(json_data['response']['body']['item']) == 2:
        upper_stopping_time = json_data['response']['body']['item'][1]['stoppingTime']
    else:
        upper_stopping_time = 0
    return [station_name,lowwer_stopping_time,upper_stopping_time]

def main():
    code_list = list(STATION_CODE.SCODE)
    csv = pd.DataFrame(columns=['역사명','하행 대기시간','상행 대기시간'])
    for code in code_list:
        station_tuple = get_tuple(code)
        csv = csv.append({'역사명':station_tuple[0],'하행 대기시간':station_tuple[1],'상행 대기시간':station_tuple[2]},ignore_index=True)
    csv.to_csv('getData/data/역별_정차시간.csv',encoding='utf8')

if __name__=='__main__':
    main()
import os
import sys
import urllib.request
import urllib.parse
import datetime
import time
import json

cilent_id = 'ZXSDm8tUd9A5DceOnMb2'
cilent_secret = 'PNbgyDA7G8'

# Url 접속 요청 후 응답 리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header('X-Naver-Client-Id', cilent_id)
    req.add_header('X-Naver-Client-Secret', cilent_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print(f'[{datetime.datetime.now()}] Url Requests Success')
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for Url : {url}')
        return None

def getNaverSearch(node,srcText,start,display):
    base = 'https://openapi.naver.com/v1/search'
    node = f'/{node}.json'
    text = urllib.parse.quote(srcText) # url 주소에 맞게 파싱
    parameters = f'?query={text}&start={start}&display={display}'

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if(responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

def getPostData(post,jsonResult,cnt):
    title = post['title']
    description = post['description']
    originallink = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S') # 2022-08-02 15:14:00

    jsonResult.append({'cnt':cnt,'title':title,'description':description,'originallink':originallink,'link':link,'pDate':pDate})
    return

def main():
    node = 'news'
    srcText = input('검색어를 입력하세요 : ')
    cnt = 0
    jsonResult = []
    jsonResponse = getNaverSearch(node, srcText, 1, 50)
    total = jsonResponse['total'] # 검색된 뉴스 갯수

    while ((jsonResponse != None) and (jsonResponse['display'] != 0 )):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)

        start = jsonResponse['start']+jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 50)
    
    print(f'전체 검색 : {total} 건')

    with open(f'data/{srcText}_naver_{node}.json',mode='w',encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult,indent=4,sort_keys=True,ensure_ascii=False)
        outfile.write(jsonFile)

    print(f'가져온 데이터 : {cnt} 건')
    print(f'{srcText}_naver_{node}.json SAVED')
    # jsonRes = getNaverSearch(node, srcText, 1, 50)
    # print(jsonRes)


if __name__=='__main__':
    main()

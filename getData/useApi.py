import pandas as pd
import urllib.request
import datetime
import json

# 변수 관리
Servicekey = ''
COLUMN_NAMES = ['상태명','상점명','대분류','중분류','업종명(소분류)','주소','개업일','폐업일','좌표']

def getRequestUrl(url):
    '''
    Url 접속 요청 후 응답 리턴 함수
    ---------------------------------
    parameter : url -> OpenAPI 전체 url
    '''
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print(f'[{datetime.datetime.now()}] Url Requests Success')
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for Url : {url}')
        return None


def getStoreInfo(getRows,pageNums):
    # 요청 url
    service_url = 'http://apis.data.go.kr/6260000/BusanCommercialHistoryService/getCommercialHistoryList'
    params = f'?serviceKey={Servicekey}'
    params += f'&numOfRows={getRows}'
    params += f'&pageNo={pageNums}'
    params += f'&resultType=json'
    url = service_url+params

    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)


def buildDataframe(jsonText):
    jsonLists = jsonText['getCommercialHistoryList']['body']['items']['item']
    dataframe = pd.DataFrame(columns = COLUMN_NAMES)
    idx = 0
    for jsonList in jsonLists:
        dataframe.loc[idx] = jsonList.values()
        idx += 1
    
    return dataframe

def main():
    rows = int(input('한 페이지에 출력할 튜플의 갯수를 입력하세요 : '))
    idx = 1
    
    dataframe = pd.DataFrame(columns=COLUMN_NAMES)

    while True:
        typejson = getStoreInfo(rows, idx)
        if typejson == None:
            break
        newDataframe = buildDataframe(typejson)
        dataframe = pd.concat([dataframe,newDataframe],ignore_index=True)
        dataframe.to_excel('data/total_data/부산광역시_상권 점포이력정보.xlsx')
        print(str(idx)+'---------'*5)
        idx += 1

if __name__=='__main__':
    main()
    pass
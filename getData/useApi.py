import pandas as pd
import urllib.request
import datetime
import json

# 변수 관리
Servicekey = 'GqnJtrJmr9aDL2eqb6lEVP4OaxCX7MR5jUMHLCMy4mUhDis9Ps90aXp8mA2M9WM%2BFw6LLzmutOTOMqpkr0PunQ%3D%3D'
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
    # 1000개씩 1~287 288~855 번까지 진행 
    idx = 282
    
    dataframe = pd.read_csv('data/total_data/부산광역시_상권 점포이력정보.xlsx',encoding='cp949',index_col=0)

    while True:
        typejson = getStoreInfo(rows, idx)
        if typejson == None:
            break
        newDataframe = buildDataframe(typejson)
        dataframe = pd.concat([dataframe,newDataframe],ignore_index=True)
        newDataframe.to_csv('data/total_data/부산광역시_상권 점포이력정보_1.xlsx',encoding='cp949')
        print(str(idx)+'---------'*5)
        idx += 1
        break

if __name__=='__main__':
    main()
    pass
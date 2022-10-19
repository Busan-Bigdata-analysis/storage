import pandas as pd
import os
import re

# data file 경로 
# project-disribution -> data -> totaldata -> 파일 위치
def get_file():
    '''
        data/total_data/ 경로 아래에 있는 파일이름들을 출력하는 함수
    '''
    while True:
        file_list = os.listdir('data/total_data/')
        for idx in range(len(file_list)):
            print(f'{idx+1} : {file_list[idx]}')
        print()
        use_file = int(input("선택할 파일의 번호를 입력하세요 : ")) - 1
        if -1 < use_file < len(file_list):
            return file_list[use_file]


def build_dataframe(file_name):
    '''
        호출한 파일로 데이터 프레임을 생성해서
        해당하는 데이터 프레임의 열 값을 출력하는 함수
    '''
    if re.search('xlsx', file_name):
        df = pd.read_excel(f'data/total_data/{file_name}')
    elif re.search('csv', file_name):
        df = pd.read_csv(f'data/total_data/{file_name}',encoding='utf-8')
    else:
        print('열수 없는 파일입니다.')
    
    return df

def append_dataframe(df):
    while True:    
        columns = list(df.columns)
        for idx in range(len(columns)):
            print(f'{idx+1} : {columns[idx]}')
        use_column = int(input('선택할 열의 번호를 입력하세요 : '))-1
        if -1 < use_column < len(columns):
            break
    df = df.dropna(subset=[columns[use_column]])
    return columns[use_column],df


def get_grade(df,col_name):
    grade = col_name+' 레벨'
    df[grade] = round(round(df[col_name].rank(pct=True),2)*10,0)
    return df


if __name__=='__main__':
    # 파일을 선책하기 위한 함수 호출
    file_name = get_file()
    # dataframe을 만들기 위한 함수 호출
    data = build_dataframe(file_name)

    break_po = 0
    while True:
        # 선택한 컬럼명,원래의 데이터 프레임을 얻기 위한 코드
        column_name,data = append_dataframe(data)
        # 선택한 데이터 컬럼의 레벨을 매겨서 반환하는 코드
        total_dataFrame = get_grade(data, column_name)
        
        break_po = int(input("1.완료 | 2.계속 : "))
        if break_po==1:
            break
    
    total_dataFrame.to_csv(f'data/total_data/{file_name}'+'_handling.xlsx',encoding='cp949')


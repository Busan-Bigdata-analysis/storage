from random import *
import pandas as pd
import numpy as np
import scipy.stats as stats
import statistics
import os
import re

# 전역변수

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
        df = pd.read_csv(f'data/total_data/{file_name}')
    else:
        print('열수 없는 파일입니다.')
    
    while True:    
        columns = list(df.columns)
        for idx in range(len(columns)):
            print(f'{idx+1} : {columns[idx]}')
        use_column = int(input('선택할 열의 번호를 입력하세요 : '))-1
        if -1 < use_column < len(columns):
            break
    df = df.dropna(subset=[columns[use_column]])
    return columns[use_column],df[columns[use_column]].astype(int)

def get_grade(column):
    '''
        등급을 얻는데 사용하는 함수
        선택한 열의 값을 등급으로 변환
    '''
    z_scores = list(stats.zscore(column,nan_policy='omit'))
    column = list(column)
    grade = []
    for idx in range(len(column)):
        if z_scores[idx]:
            score = int(z_scores[idx]*2+5)
            grade.append([list(column)[idx],score])
    return grade
    pass

def output_grade_df(name,grade):
    '''
        두개의 열을 가진 DataFrame을 생성
        [ 원래의 값 | 분류된 값 ] 형태로 생성
    '''
    return pd.DataFrame(grade,columns=[name,'등급'])
    pass

if __name__=='__main__':
    file_name = get_file()
    column_name,get_column = build_dataframe(file_name)
    grade = get_grade(get_column)
    df = output_grade_df(column_name,grade)
    print(df)
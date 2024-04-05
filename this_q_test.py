# importing date class from datetime module
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import time
import re

class make_this_quarter_num:
    def __init__(self):
        pass

    def make_this_q_num(self):
        ## 이번 달이 몇 분기인지 구하기
        # year = math.ceil(currentYear())
        quarter = math.ceil(self.currentMonth() / 3.0)
        # 조회대상연도, 조회대상 분기 리턴
        this_year, recent_quarter = self.confirm_current_year_quarter(quarter)
        return this_year, recent_quarter

    # 현재 월 반환 함수
    def currentMonth(self):
        now = time.localtime()
        return now.tm_mon

    # 현재 월만 반환
    def confirm_current_year_quarter(self, quarter):
        """이익모멘텀 대상되는 현재분기값 산출"""
        # creating the date object of today's date
        todays_date = date.today()
        # printing todays date
        # print("Current date: ", todays_date)
        # fetching the current year, month and day of today
        print("현재연도는:", todays_date.year, '년 입니다.')
        this_year = todays_date.year
        # print("Current month:", todays_date.month)
        # print("Current day:", todays_date.day)
        recent_quarter = quarter
        print('조회대상분기는', recent_quarter, '입니다.')
        return this_year, recent_quarter

def find_recent_ym(df, current_month):
    month_list = df['년월'].unique().tolist()
    month_list = [int(ym) for ym in month_list]
    month_list.sort(reverse=True)
    
    for ym in month_list:
        if ym <= current_month:
            recent_ym = ym
            break
    
    return recent_ym

def extract_performance(df, recent_ym):
    performance_cols = ['매출액', '영업이익', '순이익']
    recent_df = df[df['년월'] == recent_ym]
    recent_performance = recent_df[recent_df.columns.isin(['년월'] + performance_cols)]
    recent_performance = recent_performance[~recent_performance['매출액'].str.contains('E', na=False)]
    
    return recent_performance

def find_ym_cols(df):
    ym_cols = []
    for col in df.columns:
        if re.search(r'\d{4}년\d{2}월', col):
            ym_cols.append(col)
    
    ym_cols.sort(key=lambda x: int(re.sub(r'[^0-9]', '', x)), reverse=True)
    return ym_cols

if __name__=="__main__":
    q_num = make_this_quarter_num()
    this_year, recent_quarter = q_num.make_this_q_num()
    
    # input 폴더에서 파일 읽기
    input_folder = 'input'
    file_list = os.listdir(input_folder)
    
    if len(file_list) > 0:
        file_path = os.path.join(input_folder, file_list[0])
        
        # 파일 인코딩 방식 지정
        df = pd.read_excel(file_path)
        
        # 현재 월 가져오기
        current_month = q_num.currentMonth()
        
        # 연월 관련 컬럼 추출 및 정렬
        ym_cols = find_ym_cols(df)
        print("연월 관련 컬럼:", ym_cols)
        
        # 최근 연월 찾기
        recent_ym = find_recent_ym(df, current_month)
        
        # 최근 연월 기준 실적지표 추출
        recent_performance = extract_performance(df, recent_ym)
        
        print(recent_performance)
    else:
        print("input 폴더에 파일이 없습니다.")
# importing date class from datetime module
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math, time



class make_this_quarter_num:
    def __init__(self):
        pass

    def make_this_q_num(self):
        ## 이번 달이 몇 분기인지 구하기
        # year = math.ceil(currentYear())
        quarter = math.ceil(self.currentMonth() / 3.0)
        # 
        selected_cols_yoy_qoq_current_before_adjusted = self.confirm_current_year_quarter(quarter)
        pass

    # 현재 월 반환 함수
    def currentMonth(self):
        now = time.localtime()
        return now.tm_mon # 현재 월만 반환


    def confirm_current_year_quarter(self, quarter):
        """이익모멘텀 대상되는 현재분기값 산출"""
        # creating the date object of today's date
        todays_date = date.today()
            
        # printing todays date
        # print("Current date: ", todays_date)
            
        # fetching the current year, month and day of today
        print("Current year:", todays_date.year)
        # print("Current month:", todays_date.month)
        # print("Current day:", todays_date.day)

        조회대상분기 = quarter - 1
        print(조회대상분기)

        """이전분기까지 yoy qoq 산출"""
        selected_cols = [cols for cols in df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.columns.tolist() if ('영업이익' in cols) or ('순이익' in cols)]
        selected_cols_yoy_qoq = [cols for cols in selected_cols if ('YOY' in cols) or ('QOQ' in cols)]
        current_year_quarter = str(int(todays_date.year))[2:] + '년' + str(조회대상분기) + 'Q'
        print('현재연도및분기: ', current_year_quarter)  # 현재연도및분기:  21년3Q
        selected_cols_yoy_qoq_current_before = [cols for cols in selected_cols_yoy_qoq if current_year_quarter in cols]
        if '(E)' in selected_cols_yoy_qoq_current_before[0] :
            selected_cols_yoy_qoq_current_before = str(int(todays_date.year))[2:] + '년' + str(조회대상분기-1) + 'Q'
        print('확정현재연도및분기: ', selected_cols_yoy_qoq_current_before) # 확정현재연도및분기:  21년2Q

        """조정된 분기로 yoy qoq 산출"""
        selected_cols_yoy_qoq_current_before_adjusted = [cols for cols in selected_cols_yoy_qoq if selected_cols_yoy_qoq_current_before in cols]
        print('조정분기데이터:' , selected_cols_yoy_qoq_current_before_adjusted)
        
        return selected_cols_yoy_qoq_current_before_adjusted



if __name__=="__main__":
    q_num = make_this_quarter_num()
    q_num.make_this_q_num()














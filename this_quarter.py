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
        # 조회대상연도, 조회대상 분기 리턴
        this_year, recent_quarter = self.confirm_current_year_quarter(quarter)
        return this_year, recent_quarter


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
        print("현재연도는:", todays_date.year, '년 입니다.')
        this_year = todays_date.year
        # print("Current month:", todays_date.month)
        # print("Current day:", todays_date.day)

        조회대상분기 = quarter - 1
        recent_quarter = 조회대상분기
        print('조회대상분기는', 조회대상분기, '입니다.')

        return this_year, recent_quarter

        



if __name__=="__main__":
    q_num = make_this_quarter_num()
    this_year, recent_quarter = q_num.make_this_q_num()
    print(this_year, recent_quarter)














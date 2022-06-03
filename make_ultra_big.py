# 깃허브 업데이트
# 좌측 세번째 > 플러스 표시 클릭
# 위쪽 체크표시 클릭 > 커밋메시지 입력 > 클라우드 표시 클릭
# 터미널 > git push origin master

# from google.colab import drive
# drive.mount('/content/drive')

# 가상환경 설정
# python -m venv ultra
# conda create -n .\ultra python=3.9
# conda activate ultra
# conda deactivate
 

# 파이썬 안통하면 환경변수 설정
# 윈도우검색창에서 시스템 환경으로 검색
# 현재 작업폴더를 환경변수에 추가하면 됨

#  가상환경 실행
# source ./venv/Scripts/activate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
import encodings.idna


class make_ultra_big:
  def __init__(self) :
    path = os.path.dirname(os.path.abspath('__file__'))
    # print(path)
    self.INPUT_DIR = os.path.join(path, 'input')
    # print(self.INPUT_DIR)

  def run_ultra_big(self):
    self.readfile()
  
  def readfile(self):
    input_filename = os.listdir(self.INPUT_DIR)
    input_filename = [x for x in input_filename if '퀀트' in x][0]
    # print(input_filename)
    input_filename_folder = os.path.join(self.INPUT_DIR, input_filename)
    # print(input_filename_folder)
    df = pd.read_csv(input_filename_folder, encoding='utf-8')
    print(df.head(1))


if __name__ == "__main__":
  ultra_big = make_ultra_big()
  ultra_big.run_ultra_big()



# # path = '/content/drive/MyDrive/stock_kang/'퀀트데이터(전체)_20211110_052337.csv
# path = '/content/drive/MyDrive/stock_kang/'
# filename = os.listdir(path)[0]
# print(filename)
# path_filename = os.path.join(path,filename)
# df = pd.read_csv(path_filename)
# df.head()

# """ 2. 전처리 """
# ## 2.1. 시총 20% 필터링
# df_시총필터링 = df.copy()
# df_시총필터링 = df_시총필터링.sort_values(by = '시가총액 (억)', ascending=False) # (2342, 273)

# # 상위 20%
# 시총상위이십행 = int(df_시총필터링.shape[0]*0.2)
# 시총상위이십행

# df_시총필터링_상위이십퍼센트 = df_시총필터링.copy()
# df_시총필터링_상위이십퍼센트 = df_시총필터링_상위이십퍼센트.iloc[0:시총상위이십행, :]
# print(df_시총필터링.shape) # (2342, 273)
# df_시총필터링_상위이십퍼센트.shape # (468, 273)

# df_시총필터링_상위이십퍼센트.tail()


# ## 2.2. 지주사, 스팩, 금융사제외
# # df_시총필터링_상위이십퍼센트['업종 (대)'].value_counts() # 지주사

# df_시총필터링_상위이십퍼센트_지주사제외 = df_시총필터링_상위이십퍼센트.copy()

# # 지주사 아닌 것들만 필터링
# df_시총필터링_상위이십퍼센트_지주사제외 = df_시총필터링_상위이십퍼센트_지주사제외.loc[df_시총필터링_상위이십퍼센트_지주사제외['업종 (대)'] != '지주사', :]
# print(df_시총필터링_상위이십퍼센트.shape)
# print(df_시총필터링_상위이십퍼센트_지주사제외.shape)

# """3. 밸류 종합순위 산출"""
# ### 3.1. 분기 1/per, 분기1/pfcr, 1/pbr, 분기1/psr 평균순위 -> 정렬
# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위 = df_시총필터링_상위이십퍼센트_지주사제외.copy()
# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.head(1)

# def make_descending_value_rank(df, col):
#   df2 = df.copy()
#   new_col_역수 = str(col) + '_역수'
#   new_col_순위 = str(col) + '_rank'
#   df2[new_col_역수] = 1 / df2[col]

#   df2[new_col_순위] = df2[new_col_역수].rank(ascending=False) # 역수 수익률 큰 순서대로 내림차순 정렬
#   return df2



# # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.head()
# # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER_rank'] = df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER'].rank
# # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER_rank'] = df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER'].rank

# def make_value_rank(df):
#   df2 = df.copy()

#   df2 = make_descending_value_rank(df2,'발표 분기 PER')
#   df3 = make_descending_value_rank(df2,'분기 PFCR')
#   df4 = make_descending_value_rank(df3, '발표 PBR')
#   df5 = make_descending_value_rank(df4, '발표 분기 PSR')
#   df6 = df5.copy()

#   """밸류종합순위 산출"""
#   df6['밸류종합순위'] = df6[['발표 분기 PER_rank','분기 PFCR_rank','발표 PBR_rank','발표 분기 PSR_rank']].mean(axis=1)

#   return df6


# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위 = make_value_rank(df_시총필터링_상위이십퍼센트_지주사제외)
# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.head()


# """4. 이익모멘텀 종합순위 산출"""
# ### 전분기 대비 영업이익 증가율, 전년 동기 대비 영업이익 증가율, 전 분기 대비 순이익 증가율, 전년 동기 대비 순이익 증가율
# """이번달이 몇분기인지 구하기"""

# import math
# import time


# # 현재 월 반환 함수
# def currentMonth():
#   now = time.localtime()
#   return now.tm_mon # 현재 월만 반환

# #############################################
# ## 이번 달이 몇 분기인지 구하기
# #
# # year = math.ceil(currentYear())
# quarter = math.ceil( currentMonth() / 3.0 )
# print(quarter)


# # importing date class from datetime module
# from datetime import date

# def confirm_current_year_quarter():
#   """이익모멘텀 대상되는 현재분기값 산출"""
#   # creating the date object of today's date
#   todays_date = date.today()
    
#   # printing todays date
#   # print("Current date: ", todays_date)
    
#   # fetching the current year, month and day of today
#   print("Current year:", todays_date.year)
#   # print("Current month:", todays_date.month)
#   # print("Current day:", todays_date.day)

#   조회대상분기 = quarter - 1
#   print(조회대상분기)

#   """이전분기까지 yoy qoq 산출"""
#   selected_cols = [cols for cols in df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.columns.tolist() if ('영업이익' in cols) or ('순이익' in cols)]
#   selected_cols_yoy_qoq = [cols for cols in selected_cols if ('YOY' in cols) or ('QOQ' in cols)]
#   current_year_quarter = str(int(todays_date.year))[2:] + '년' + str(조회대상분기) + 'Q'
#   print('현재연도및분기: ', current_year_quarter)  # 현재연도및분기:  21년3Q
#   selected_cols_yoy_qoq_current_before = [cols for cols in selected_cols_yoy_qoq if current_year_quarter in cols]
#   if '(E)' in selected_cols_yoy_qoq_current_before[0] :
#     selected_cols_yoy_qoq_current_before = str(int(todays_date.year))[2:] + '년' + str(조회대상분기-1) + 'Q'
#   print('확정현재연도및분기: ', selected_cols_yoy_qoq_current_before) # 확정현재연도및분기:  21년2Q

#   """조정된 분기로 yoy qoq 산출"""
#   selected_cols_yoy_qoq_current_before_adjusted = [cols for cols in selected_cols_yoy_qoq if selected_cols_yoy_qoq_current_before in cols]
#   print('조정분기데이터:' , selected_cols_yoy_qoq_current_before_adjusted)
  
#   return selected_cols_yoy_qoq_current_before_adjusted

# selected_cols_yoy_qoq_current_before_adjusted = confirm_current_year_quarter()


# """랭크산출 : 내림차순 + 순위산출"""

# def make_earnings_momentum(df, selected_cols_yoy_qoq_current_before_adjusted):
#   df2 = df.copy()
#   selected_col_rank = []
#   """내림차순으로 순위부여"""
#   for col in selected_cols_yoy_qoq_current_before_adjusted:
#     print(col)
    
#     col_rank = str(col) + '_순위'
#     df2[col_rank] = df2[col].rank(ascending=False)
#     selected_col_rank.append(col_rank)

#   """순위를 평균"""
#   df2['이익모멘텀_종합순위'] = df2[selected_col_rank].mean(axis=1)

#   # df2['이익모멘텀_종합순위'] = 
#   return df2
  


# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀 = make_earnings_momentum(df_시총필터링_상위이십퍼센트_지주사제외_밸류순위, selected_cols_yoy_qoq_current_before_adjusted)
# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀.head(3)


# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀.to_csv('/content/drive/MyDrive/stock_kang/output/kang_sample.csv', encoding='cp949')

# """5. 퀄리티 종합순위 산출"""
# [x for x in df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀.columns if '자산' in x]
# def 퀄리티_종합순위_산출(df):
#   df2 = df.copy()
#   """퀄리티 종합순위 산출"""
  
#   # GPA (내림차순)
#   df2['과거GP/A_rank'] = df2['과거 GP/A (%)'].rank(ascending=False) 

#   # 자산성장률(오름차순)
#   df2['자산증가율 (최근분기)_rank'] = df2['자산증가율 (최근분기)'].rank(ascending=True) 

#   # 영업이익/차입금 증가율(내림차순)
#   df2['(영업이익/차입금) 증가율_rank'] = df2['(영업이익/차입금) 증가율'].rank(ascending=False)

#   selected_cols = ['과거GP/A_rank','자산증가율 (최근분기)_rank','(영업이익/차입금) 증가율_rank']
  
#   # 퀄리티 종합순위 산출
#   df2['퀄리티_종합순위'] = df2[selected_cols].mean(axis=1)

#   return df2

# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀_퀄리티순위 = 퀄리티_종합순위_산출(df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀)
# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀_퀄리티순위.head()



# """6. 대형주 울트라"""
# def 울트라최종순위산출(df):
#   df2 = df.copy()

#   selected_cols = ['밸류종합순위','이익모멘텀_종합순위','퀄리티_종합순위']

#   # 울트라 종합순위 산출
#   df2['울트라_종합순위'] = df2[selected_cols].mean(axis=1)
  
#   # 정렬
#   df2 = df2.sort_values(by='울트라_종합순위', ascending=True)

#   return df2

# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀_퀄리티순위_울트라최종순위 = 울트라최종순위산출(df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀_퀄리티순위)
# df_시총필터링_상위이십퍼센트_지주사제외_밸류순위_이익모멘텀_퀄리티순위_울트라최종순위.head(20)


# """
# 7. 울트라 소형주
# 3. 밸류모멘텀 산출
# 4. 퀄리티모멘텀
# 5. 밸류퀄리티
# 8. 울트라
# 다음과제 : kisve 산출
# 코스피배당수익률, 5년국채금리, 코스피 PER역수 비교 + 머신러닝 + 문병로 메트릭스튜디오 참고
# [ ]
# 1
# 강화학습 1달, 3개월, 6개월 예측
# 미국주식 미래에셋크롤링 + 최일 CFA 밸류에이션
# """

# 깃허브 업데이트
# 좌측 세번째 > 플러스 표시 클릭
# 위쪽 체크표시 클릭 > 커밋메시지 입력 > 클라우드 표시 클릭
# 터미널 > git push origin master

# 깃허브 내려받기
# git pull

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

# from builtins import EncodingWarning
from fileinput import filename
# from typing_extensions import Self
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
import encodings.idna
import this_quarter


class make_ultra_big:
  def __init__(self) :
    path = os.path.dirname(os.path.abspath('__file__'))
    # print(path)
    self.INPUT_DIR = os.path.join(path, 'input')
    self.OUTPUT_DIR = os.path.join(path, 'output')
    # print(self.INPUT_DIR)

  def run_ultra_big(self):
    """0-1. 실행함수(대형주울트라)"""
    df = self.readfile()
    df_시총20프로 = self.시총20프로필터링(df)
    df_지주스펙제외 = self.지주사스펙금융사제외(df_시총20프로)

    """1. 밸류종합순위"""
    df = self.밸류종합순위(df_지주스펙제외)
    df.reset_index(inplace=True, drop=True)

    """2. 이익모멘텀종합순위"""
    # df = df.set_index()
    filename_output = os.path.join(self.OUTPUT_DIR, 'tmp.csv')
    df.to_csv(filename_output, encoding='cp949')
  
  def readfile(self):
    input_filename = os.listdir(self.INPUT_DIR)
    input_filename = [x for x in input_filename if '퀀트' in x][0]
    # print(input_filename)
    input_filename_folder = os.path.join(self.INPUT_DIR, input_filename)
    # print(input_filename_folder)
    df = pd.read_csv(input_filename_folder, encoding='utf-8')
    # print(df.head(1))

    return df

  def 시총20프로필터링(self, df):
    df_시총필터링 = df.copy()
    df_시총필터링 = df_시총필터링.sort_values(by = '시가총액 (억)', ascending=False) # 내림차순 정렬
    시총상위이십행 = int(df_시총필터링.shape[0]*0.2)
    시총상위이십행    
    df_시총필터링_상위이십퍼센트 = df_시총필터링.copy()
    df_시총필터링_상위이십퍼센트 = df_시총필터링_상위이십퍼센트.iloc[0:시총상위이십행, :]
    # print(df_시총필터링.shape) # (2342, 273)
    # print(df_시총필터링_상위이십퍼센트.shape) # (474, 273)

    return df_시총필터링_상위이십퍼센트


  def 지주사스펙금융사제외(self, df):
    """2.2. 지주사, 스팩, 금융사제외"""
    df_시총필터링_상위이십퍼센트_지주사제외 = df.copy()
    df_시총필터링_상위이십퍼센트_지주사제외
    # 지주사 아닌 것들만 필터링
    df_시총필터링_상위이십퍼센트_지주사제외 = df_시총필터링_상위이십퍼센트_지주사제외.loc[df_시총필터링_상위이십퍼센트_지주사제외['업종 (대)'] != '지주사', :]
    # print(df.shape)
    # print(df_시총필터링_상위이십퍼센트_지주사제외.shape) # (436, 273)
    # print(df_시총필터링_상위이십퍼센트_지주사제외['업종 (대)'].value_counts())

    # 금융업종 제외
    df_시총필터링_상위이십퍼센트_지주사금융사제외 = df_시총필터링_상위이십퍼센트_지주사제외.loc[df_시총필터링_상위이십퍼센트_지주사제외['업종 (대)'] != '금융', :]
    # print(df_시총필터링_상위이십퍼센트_지주사금융사제외.shape) # (409, 273)
    # print(df_시총필터링_상위이십퍼센트_지주사금융사제외['업종 (대)'].value_counts())

    return df_시총필터링_상위이십퍼센트_지주사금융사제외

  
  def 밸류종합순위(self, df):
    """3. 밸류 종합순위 산출"""
    ### 3.1. 분기 1/per, 분기1/pfcr, 1/pbr, 분기1/psr 평균순위 -> 정렬
    df_시총필터링_상위이십퍼센트_지주사제외_밸류순위 = df.copy()
    df_시총필터링_상위이십퍼센트_지주사제외_밸류순위 = self.make_value_rank(df_시총필터링_상위이십퍼센트_지주사제외_밸류순위)
    # print(df_시총필터링_상위이십퍼센트_지주사제외_밸류순위)
    # filename = os.path.join(self.OUTPUT_DIR, 'tmp2.csv')
    # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.to_csv(filename, encoding='cp949')

    ###  밸류종합순위

    # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위.head()
    # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER_rank'] = df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER'].rank
    # df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER_rank'] = df_시총필터링_상위이십퍼센트_지주사제외_밸류순위['발표 분기 PER'].rank

    return df_시총필터링_상위이십퍼센트_지주사제외_밸류순위


  def make_value_rank(self, df):
    df2 = df.copy()
    df2 = self.make_descending_value_rank(df2,'발표 분기 PER')
    df3 = self.make_descending_value_rank(df2,'분기 PFCR')
    df4 = self.make_descending_value_rank(df3, '발표 PBR')
    df5 = self.make_descending_value_rank(df4, '발표 분기 PSR')
    df6 = df5.copy()

    df6['밸류종합순위'] = df6[['발표 분기 PER_rank','분기 PFCR_rank','발표 PBR_rank','발표 분기 PSR_rank']].mean(axis=1)

    return df6


  def make_descending_value_rank(self, df, col):
    df2 = df.copy()
    new_col_역수 = str(col) + '_역수'
    new_col_순위 = str(col) + '_rank'
    df2[new_col_역수] = 1 / df2[col]
    df2[new_col_순위] = df2[new_col_역수].rank(ascending=False) # 역수 수익률 큰 순서대로 내림차순 정렬
    return df2

  
  # """4. 이익모멘텀 종합순위 산출"""
  # ### 전분기 대비 영업이익 증가율, 전년 동기 대비 영업이익 증가율, 전 분기 대비 순이익 증가율, 전년 동기 대비 순이익 증가율
  # """이번달이 몇분기인지 구하기"""


if __name__ == "__main__":
  ultra_big = make_ultra_big()
  ultra_big.run_ultra_big()




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

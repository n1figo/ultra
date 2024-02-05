from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC   
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
import sqlite3
import urllib.parse
# from pyvirtualdisplay import Display
import time, requests, io, datetime, pickle, os, xlsxwriter


class QuantPick:
  def __init__(self):
    # path
    # self.run()
    self.today_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    # 피클저장 (날짜) 재무
    self.path = '/content/drive/My Drive/stock/'
    self.basename = 'finance_data_'
    self.filename_time = self.path + self.basename  + self.today_time + '.pkl'
    self.filename_operating = self.path + self.basename + 'for_operating.pkl'

    # 피클저장 (날짜) gpa_ocf_magic
    self.gpa_ocf_magic_filename_time = self.path + 'gpa_ocf_magic_all_' + self.today_time + '.pkl'
    self.gpa_ocf_magic_filename_operating = self.path + 'gpa_ocf_magic_all_for_operating.pkl'
    self.gpa_ocf_magic_filename_time_csv = self.path + 'gpa_ocf_magic_all_' + self.today_time + '.csv'

    # 피클저장 (시가총액)
    self.market_filename_time = self.path + 'market_cap_pbr_' + self.today_time + '.pkl'
    self.market_filename_operating = self.path + 'market_cap_pbr_for_operating.pkl'

    # 피클저장 (200 리스트)
    self.gpa_magic_ocf_200_list_daily_filename = self.path + 'gpa_ocf_magic_200_list_' + self.today_time + '.pkl'
    self.gpa_magic_ocf_200_list_daily_filename_xlsx = self.path + 'gpa_ocf_magic_200_list_' + self.today_time + '.xlsx'

    """ 종목코드 산출 """
    self.code_list, self.code_name_df = self.get_stock_codes()
    print('---- 종목코드 ----')
    
    # 임시코드
    # self.code_list = self.code_list[0:2]
    # self.code_list = self.code_list[0:10]
    # self.code_list = self.code_list[0:500]
    # self.code_list = ['A003690','A012690']
    # self.code_list = ['A014680']
    # print("*"*50)
    # print("---테스트할 종목코드입니다.---")
    # print(self.code_list)
    # print("*"*50)
    
  def gather(self):
    """ A. 퀀트정보 파싱 및 가공(3개월에 한번)"""
    # 전종목 gpa, ocf, 마법공식 필요정보 파싱
    # gpa_dict, ocf_a_dict, roic_dict, op_dict, net_debt_dict, finance_dict
    self.gpa, self.ocf_a, self.roic, self.op, self.net_debt, self.finance_dict = self.all_gpa_ocf_a()

    # 재무정보 저장
    finance_data = {}
    finance_data['gpa'] = self.gpa
    finance_data['ocf_a'] = self.ocf_a
    finance_data['roic'] = self.roic
    finance_data['op'] = self.op
    finance_data['net_debt'] = self.net_debt
    finance_data['finance_dict'] = self.finance_dict

    # 재무정보 피클저장 (날짜)    
    with open(self.filename_time, 'wb') as handle:
      pickle.dump(finance_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # 재무정보 피클저장 (운영용)
    with open(self.filename_operating, 'wb') as handle:
      pickle.dump(finance_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('---스크래핑 된 재무 데이터가 피클로 저장되었습니다.---')

    return finance_data


  def run(self):
    """B. 실행파일 : pkl파일 있는지 없는지로 시작 + 퀀트전체산출물 저장"""
    # 전종목 시가총액, per, pbr 추출 (매일)
    all_market_cap_pbr_dict = {}
    self.all_market_cap, self.all_pbr = self.parsing_all_market_cap_PBR(self.code_list)
    all_market_cap_pbr_dict['시가총액'] = self.all_market_cap
    all_market_cap_pbr_dict['pbr'] = self.all_pbr
    print('---시총, pbr 딕셔너리 출력----')
    print(all_market_cap_pbr_dict)  # {'시가총액': {'A014680': 12142.0}, 'pbr': {'A014680': ['3.18']}}

    # 시가총액, PBR 수치 저장 (날짜)
    with open(self.market_filename_operating, 'wb') as handle:
      pickle.dump(all_market_cap_pbr_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # gpa, ocf, 마법공식, 벨류에이션 병합 데이터 산출 + PER, PSR, POR, PCR 산출
    gpa_ocf_magic_value_all = self.gather_data_to_dataframe()

    # 업종코드 산출
    industry_code_df = self.get_krx_industry_code()

    # 업종코드 결합 후 평균 산출
    gpa_ocf_magic_value_all_indust_avg = self.calculate_industry_average(industry_code_df, gpa_ocf_magic_value_all)

    # 퀀트 산출물 피클 저장 (날짜)
    with open(self.gpa_ocf_magic_filename_time, 'wb') as handle:
      pickle.dump(gpa_ocf_magic_value_all_indust_avg, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # 퀀트 산출물 피클 저장 (운영)
    with open(self.gpa_ocf_magic_filename_operating, 'wb') as handle:
      pickle.dump(gpa_ocf_magic_value_all_indust_avg, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # 엑셀저장
    gpa_ocf_magic_value_all_indust_avg.to_csv(self.gpa_ocf_magic_filename_time_csv, encoding='cp949')

    return gpa_ocf_magic_value_all_indust_avg

    
  def final_200_list(self, df):
    """C. 실행파일 : 최종200리스트 산출 및 저장"""
    # 최종 200 리스트 산출
    magic_200_list, gpa_pbr_200_list, ocf_a_pbr_200_list, df_new = self.make_magic_gpa_ocf_a_200_list(df)

    # 저장 (피클 200리스트)
    with open(self.gpa_magic_ocf_200_list_daily_filename, 'wb') as handle:
      pickle.dump(magic_200_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
      pickle.dump(gpa_pbr_200_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
      pickle.dump(ocf_a_pbr_200_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
      pickle.dump(df_new, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # 저장 (csv 200리스트)
    writer = pd.ExcelWriter(self.gpa_magic_ocf_200_list_daily_filename_xlsx, engine='xlsxwriter')

    magic_200_list.to_excel(writer, sheet_name='magic_200')
    gpa_pbr_200_list.to_excel(writer, sheet_name='gpa_pbr_200')
    ocf_a_pbr_200_list.to_excel(writer, sheet_name='ocf_a_pbr_200')

    writer.save()

    return magic_200_list, gpa_pbr_200_list, ocf_a_pbr_200_list, df_new



    

  
  def get_stock_codes(self):
    """1. 종목코드 스크래핑"""
    # 전종목 코드 다운
    self.MARKET_CODE_DICT = {
        'kospi': 'stockMkt',
        'kosdaq': 'kosdaqMkt',
        'konex': 'konexMkt'
    }

    self.DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

    # 종목코드, 종목명 데이터프레임 저장
    code_name_df = self.parsing_stock_codes()

    # 종목코드에 A 붙이기
    code_list = []
    for c in code_name_df.종목코드:
        new_code = 'A' + str(c)
        code_list.append(new_code)

    return code_list, code_name_df


  def download_stock_codes(self, market=None, delisted=False):
      params = {'method': 'download'}

      if market.lower() in self.MARKET_CODE_DICT:
          params['marketType'] = self.MARKET_CODE_DICT[market]

      if not delisted:
          params['searchType'] = 13

      params_string = urllib.parse.urlencode(params)
      request_url = urllib.parse.urlunsplit(['http', self.DOWNLOAD_URL, '', params_string, ''])

      df = pd.read_html(request_url, header=0)[0]
      df.종목코드 = df.종목코드.map('{:06d}'.format)

      return df


  def parsing_stock_codes(self):
      kospi_stocks = self.download_stock_codes('kospi')
      kosdaq_stocks = self.download_stock_codes('kosdaq')
      code_name = pd.concat([kospi_stocks[['회사명', '종목코드']], kosdaq_stocks[['회사명', '종목코드']]], axis=0)
      return code_name


  def calculate_roic(self, soup, df_재무_all):
    """2.1. 마법공식(자본수익률 산출)"""
    ###################
    # 1. 유형자산 파싱
    ###################
    final_added_acc = []

    # 재무상태표 > 세부항목 들어가기
    rows_2 = soup.findAll('tr', {'class':'c_grid2_3 rwf acd_dep2_sub'})
    for row_2 in rows_2:
        # 계정명
        headers = [x for x in row_2.find_all('th')]
        selected_acc = headers[0].text.strip()

        # 유형자산 이름 파싱
        added_acc = []
        if '유형자산' in selected_acc:
            added_acc.append(selected_acc)

            # 유형자산 세부숫자 파싱
            td = row_2.find_all('td')
            for t in td:
                added_acc.append(t.text)
        else:
            continue

        # Ic 항목에 한줄추가 (순운전자본, 순고정자산)
        final_added_acc.append(added_acc)

    ###########################################
    # 2. 재고자산, 매출채권및기타유동채권 파싱
    ###########################################
    # 재무상태표 > 유동자산 세부항목 
    rows = soup.findAll('tr', {'class':'c_grid2_2 rwf acd_dep2_sub'})
    for row in rows:
        # 계정명
        headers = [x for x in row.find_all('th')]
        selected_acc = headers[0].text.strip()

        # 재고자산, 매출채권 계정명 파싱
        added_acc = []
        if ('재고자산' in selected_acc) or ('매출채권' in selected_acc):
            # 헤더 파싱
            added_acc.append(selected_acc)

            # 재고자산, 매출채권 옆 숫자파싱
            td = row.find_all('td')
            for t in td:
                # print(t.text)
                added_acc.append(t.text)
        else: 
            continue

        # 최종추가할 항목에 한줄추가 (순운전자본, 순고정자산)
        final_added_acc.append(added_acc)

    #################################
    # 3. 매입채무및기타유동채무 파싱
    #################################
    # 재무상태표 > 유동자산 세부항목 유동금융부채
    rows_3 = soup.findAll('tr', {'class':'c_grid2_6 rwf acd_dep2_sub'})
    for row_3 in rows_3:
        # 계정명
        headers = [x for x in row_3.find_all('th')]
        selected_acc = headers[0].text.strip()

        # 매입채무및기타유동채무 이름 파싱
        added_acc = []
        if '매입채무및기타유동채무' in selected_acc:
            added_acc.append(selected_acc)

            # 매입채무및기타유동채무 숫자 파싱
            td = row_3.find_all('td')
            for t in td:
                added_acc.append(t.text)
        else:
            continue

        # 최종추가할 항목에 한줄추가 (순운전자본, 순고정자산)
        final_added_acc.append(added_acc)

    #####################################
    # 4. ROIC에서 IC(투하자본: 영업자산)
    #####################################
    final_added_acc = pd.DataFrame(final_added_acc)
    # final_added_acc
    
    # 최근항목 iclist에 저장
    ic_list = final_added_acc.iloc[:,-1]
    
    # ,삭제 및 계산가능하게 float 전환 
    float_ic_list = [str(x).replace(',','') for x in ic_list]
    float_ic_list_real = [float(x) for x in float_ic_list]
    
    # IC(투하자본) 계산
    ic  = sum(float_ic_list_real[0:3]) - float_ic_list_real[3]
    
    # roic 계산
    df_재무_all = df_재무_all.set_index(df_재무_all.columns[0])
    ret = df_재무_all['최근1년']['영업이익']
    
    # roic 계산
    roic = ret/ic
    roic

    return roic, ret


  # 1. 순이자부채
  def get_earning_yields_op_netdebt(self, soup, df_재무_all):
    ####################################
    """2.2. 마법공식(이익수익률 산출)"""
    ####################################
    final_added_acc = []
    # 1) 단기사채, 단기차입금, 유동성장기부채, 유동금융부채, 기타유동부채
    rows = soup.findAll('tr', {'class':'c_grid2_6 rwf acd_dep2_sub'})
    
    # 계정항목을 하나씩 돌아가면서 검사
    for row in rows:
      # 계정명
      headers = [x for x in row.find_all('th')]
      # 계정명 텍스트 저장
      selected_acc = headers[0].text.strip()

      # 순이자부채 항목명 파싱
      added_acc = []
      debt_list = ['단기사채', '단기차입금', '유동성장기부채', '유동금융부채', '기타유동부채']
      
      # 원하는 부채항목명이 있는지 검사
      if selected_acc in debt_list:
          # 원하는 항목이 있으면 리스트에 추가
          added_acc.append(selected_acc)

          # 원하는 부채항목 숫자 파싱
          td = row.find_all('td')
          for t in td:
              added_acc.append(t.text)
      else:
          continue

      # 데이터프레임으로 만들 항목에 한줄추가 (순이자부채 항목 1줄)
      final_added_acc.append(added_acc)
    
    # 2) 사채, 장기차입금, 비유동금융부채, 기타비유동부채 
    rows = soup.findAll('tr', {'class':'c_grid2_7 rwf acd_dep2_sub'})
    # 계정항목을 하나씩 돌아가면서 검사
    for row in rows:
      # 계정명
      headers = [x for x in row.find_all('th')]
      # 계정명 텍스트 저장
      selected_acc = headers[0].text.strip()

      # 순이자부채 항목명 파싱
      added_acc = []
      debt_list = ['사채', '장기차입금', '비유동금융부채', '기타비유동부채']
      
      # 원하는 부채항목명이 있는지 검사
      if selected_acc in debt_list:
          # 원하는 항목이 있으면 리스트에 추가
          added_acc.append(selected_acc)

          # 원하는 부채항목 숫자 파싱
          td = row.find_all('td')
          for t in td:
              added_acc.append(t.text)
      else:
          continue
          
      # 데이터프레임으로 만들 항목에 한줄추가 (순이자부채 항목 1줄)
      final_added_acc.append(added_acc)
        
    # 3) 데이터프레임으로 만들고 rowsum 이후 맨 마지막 항목 추출
    final_added_acc = pd.DataFrame(final_added_acc)
    # final_added_acc = final_added_acc.fillna(0)
    # print(final_added_acc)
    
    # 4) 맨 마지막 항목 추출
    net_debt_list = final_added_acc.iloc[:,-1]
    net_debt_list_modified = [str(x).replace(',','') for x in net_debt_list]
    net_debt_list_modified_2 = [x.replace('\xa0','0') for x in net_debt_list_modified]
    print(net_debt_list_modified_2)
    net_debt_list_float = [float(x) for x in net_debt_list_modified_2]
    net_debt = sum(net_debt_list_float)
    
    return net_debt

  
  
  # 최근 4개 분기 재무정보 스크래핑 + sql 저장
  def one_firm_gpa_ocf_a_magic(self, code):
    ##########################################
    """3-1. 최근 4개분기 재무정보 스크래핑"""
    ##########################################
    # 최근 분기 재무제표
    # 연결
    # recent_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'.format(code)
    # 개별
    recent_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701'.format(code)
    # 샘플 url : https://comp.fnguide.com/SVO2/asp/SVD_Finance.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701

    # 서버 버전 headless 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"')
    chrome_options.add_argument("--lang=ko_KR")
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",chrome_options=chrome_options)

    driver.implicitly_wait(3)
    driver.get(recent_url)

    """
    # PC버전 옵션
    # headless option 지정
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options, executable_path="C:\\Program Files (x86)\\Mozilla Firefox\\geckodriver-v0.25.0-win64\\geckodriver.exe")
    
    print("Firefox Headless Browser Invoked")
    driver.get(recent_url)
    """
    # 1. 분기 손익계산서 클릭 : click by id "btnSonik_Q"
    # 총 자산 가져오기
    """
    driver.find_element_by_id("btnSonik_Q").click()
    driver.find_element_by_id("btnDaecha_Q").click()
    driver.find_element_by_id("btnCash_Q").click()
    """

    #####################################
    # 최근 손익정보 합치기 (최신 1년)
    #####################################
    html = driver.page_source
    driver.quit()
    print("driver has been quit!")
    soup = BeautifulSoup(html, 'html5lib')
    table_손익 = soup.find_all(id='divSonikQ')

    # 2. 매출총이익 스크래핑
    # 재무정보 테이블화 (beautifuklsoup resultset은 문자열로 전환해줘야 한다!)
    table_손익 = pd.read_html(str(table_손익))

    # 테이블에서 0번 항목만 내리기
    df_손익 = table_손익[0]
    df_손익 = df_손익.set_index(df_손익.columns[0])

    # 전년동기 정보 삭제
    selected_cols = [x for x in df_손익.columns if '전년동기' not in x]
    df_손익_selected = df_손익[selected_cols]

    # 최근 4분기 정보합치기
    df_손익_selected['최근1년'] = df_손익_selected.sum(axis=1)

    # gpa 에서 grossprofit 구하기
    gross_profit = df_손익_selected['최근1년']['매출총이익']

    # 최근 4분기 매출액, 영업이익, 순이익 저장 (★★★★ 테스트필요 ★★★★)
    print(df_손익_selected)
    recent_sales = df_손익_selected['최근1년']['매출액']
    recent_op_margin = df_손익_selected['최근1년']['영업이익']
    recent_profit = df_손익_selected['최근1년']['당기순이익']
    # recent_profit = df_손익_selected['최근1년']['지배주주순이익']

    # 딕셔너리 저장
    recent_dict = {}
    recent_dict[code]= {'매출액':recent_sales}
    recent_dict[code].update({'영업이익':recent_op_margin})
    recent_dict[code].update({'당기순이익':recent_profit})
    # recent_dict[code].update({'지배주주순이익':recent_profit})
    # print("*"*50)
    # print("dictionary scraping is ok!!")
    # print("*"*50)
    
    #################################
    # 3. 총자산 스크래핑
    #################################
    # 테이블 스크래핑할 때는 str으로 전환 필수 + read_html 읽으면 0번째 항목을 저장할 것!
    table_재무상태 = soup.find_all(id='divDaechaQ')
    table_재무상태 = pd.read_html(str(table_재무상태))

    # 테이블에서 0번째 항목 저장
    df_재무상태 = table_재무상태[0]
    df_재무상태 = df_재무상태.set_index(df_재무상태.columns[0])
    df_재무상태_selected = df_재무상태.copy()
    df_재무상태_selected['최근1년'] = df_재무상태_selected.iloc[:,-1]

    # 자산 스크래핑
    asset = df_재무상태.iloc[:, -1]['자산']

    # 4. gpa
    gpa_onefirm = gross_profit / asset
    sample_gpa = []
    sample_gpa.append(gpa_onefirm)

    gpa = {}
    gpa[code] = sample_gpa
    # print("*"*50)
    # print("gpa scraping is ok!!")
    # print("*"*50)
    
    #########################
    # 5. 현금흐름표 스크래핑
    #########################
    table_현금흐름 = soup.find_all(id='divCashQ')
    table_현금흐름 = pd.read_html(str(table_현금흐름))

    # 테이블에서 0번째 항목 저장
    df_현금흐름 = table_현금흐름[0]
    df_현금흐름 = df_현금흐름.set_index(df_현금흐름.columns[0])

    # 최근 1년 현금흐름 합산
    df_현금흐름['최근1년'] = df_현금흐름.sum(axis=1)
    ocf = df_현금흐름['최근1년']['영업활동으로인한현금흐름']
    ocf_a_onefirm = ocf / asset
    sample_ocf_a = []
    sample_ocf_a.append(ocf_a_onefirm)

    ocf_a = {}
    ocf_a[code] = sample_ocf_a
    
    # 최근1년 영업흐름 저장
    recent_dict[code].update({'영업현금흐름':ocf})
    
    ###########################################
    # 6. 재무상태표 + 손익 + 현금흐름표 결합 # 
    ###########################################
    df_재무_all = pd.concat([df_손익_selected, df_재무상태_selected, df_현금흐름], axis=0)

    # 7. 인덱스명 수정 (에 참여한 계정 펼치기)
    df_재무_all = df_재무_all.reset_index()
    col_0 = df_재무_all.columns.tolist()[0]
    df_재무_all[col_0] = df_재무_all[col_0].str.replace('계산에 참여한 계정 펼치기','')

    # 8. 마법공식 roic 구하기
    roic, operating_profit  = self.calculate_roic(soup, df_재무_all)
    roic_dict = {}
    operating_profit_dict = {}
    net_debt_dict = {}

    # 마법공식 : 이익수익률 구하기 (영업이익 / 시가총액 + 부채)    
    # 마법공식 : 순이자부담부채 
    net_debt = self.get_earning_yields_op_netdebt(soup, df_재무_all)
    
    # 리스트화 
    sample_roic = []
    sample_op = []
    sample_net_debt = []
    sample_roic.append(roic) 
    sample_op.append(operating_profit)
    sample_net_debt.append(net_debt)
    
    # 딕셔너리화
    roic_dict[code] = sample_roic
    operating_profit_dict[code] = sample_op
    net_debt_dict[code]= sample_net_debt
    
    print(gpa, ocf_a, roic_dict, operating_profit_dict, net_debt_dict, recent_dict)
    print("*"*50)
    print("one firm gpa is ok!!!")
    print("*"*50)
    
    return gpa, ocf_a, roic_dict, operating_profit_dict, net_debt_dict, recent_dict

  
  def all_gpa_ocf_a(self):
    ##########################################
    """3-2. 전종목 gpa, ocfa 크롤링"""
    ##########################################
    gpa_dict = {}
    ocf_a_dict = {}
    roic_dict = {}
    op_dict = {}
    net_debt_dict = {}
    finance_dict = {}
    for idx, code in enumerate(self.code_list):
    # for idx, code in enumerate(['A155660','A005930']):
        print(idx, code)
        try:
          # 개별 기업 gpa 계산 (5~6시간 짜리 작업)
          gpa_one, ocf_a_one, roic_one, op_one, net_debt_one, recent_dict_one = self.one_firm_gpa_ocf_a_magic(code)
          print("*"*50)
          print("---------recent_dict_one---------")
          print(recent_dict_one)
          print("*"*50)
          # 전체기업 gpa 리스트 업데이트
          gpa_dict.update(gpa_one)
          ocf_a_dict.update(ocf_a_one)
          roic_dict.update(roic_one)
          op_dict.update(op_one)
          net_debt_dict.update(net_debt_one)
          finance_dict.update(recent_dict_one)
          
        except :
          print(code, "error occurred!")
          continue   
        
    
    return gpa_dict, ocf_a_dict, roic_dict, op_dict, net_debt_dict, finance_dict

  
  def get_PBR(self, code):
    ##########################################
    """4-1. 1종목 pbr 스크래핑"""
    ##########################################
    pbr = {}
    sample_pbr = []
    # 최근 PBR 수치 스크래핑
    pbr_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701'.format(code)
    html = requests.get(pbr_url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # PBR 포함된 메뉴항목 크롤링
    corp_group2 = soup.find_all(id='corp_group2')
    
    # 계정명 탐색
    for acc_name in corp_group2:
        # 한글 계정명
        dt = acc_name.find_all('dt')
        # 숫자
        dd = acc_name.find_all('dd')
        
    # 계정명 PBR 인 항목의 숫자를 저장
    for idx, (t, d) in enumerate(zip(dt, dd)):
        if t.text.strip().endswith('PBR(Price Book-value Ratio)'): 
            # print(idx, t.text.strip(), d.text.strip())
            sample_pbr.append(d.text.strip())
            pbr[code] = sample_pbr
            
    return pbr


  # 전종목 pbr 구하는 함수
  def all_pbr(self):
    ##########################################
    """4-2. 전종목 PBR 구하기"""
    ##########################################
    pbr_dict = {}
    for idx, code in enumerate(code_list):
        try:
            # 개별기업 PBR 딕셔너리 계산
            pbr_one = self.get_PBR(code)
            print(idx, pbr_one)
            # 전체기업 pbr 딕셔너리 업데이트
            pbr_dict.update(pbr_one)
        except :
            continue
    return pbr_dict

  
  # 전종목 시가총액, per, pbr 추출
  def get_market_cap_PBR(self, code):
    #####################################################
    """5. 시가총액, PBR 스크래핑 + PER, PCR, PSR 계산"""
    #####################################################
    market_cap = {}
    sample_market_cap = []

    per = {}
    sample_per = []

    pbr = {}
    sample_pbr = []

    pcr = {}
    sample_pcr = []
    
    psr = {}
    sample_psr = []
    
    ########################
    # 1. 시가총액 스크래핑 #
    ########################
    # 연결
    market_cap_url = 'https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'.format(code)
    # 개별?
    # market_cap_url = 'https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=B&NewMenuID=101&stkGb=701'.format(code)
    response = requests.get(market_cap_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # 1.1. 시가총액 포함 영역 파싱
    market_grid = soup.find_all(id='svdMainGrid1')
        #svdMainGrid1 > table > tbody > tr:nth-child(5) > td:nth-child(2)
    
    # 1.2. soup 에서 read_html로 테이블을 추출할 수 있음
        # 이때 링크는 string으로 전환해야 함
        # 중첩리스트 일 수 있기 때문에 [0]을 추가해줌
    table_시총 = pd.read_html(str(market_grid))
    market_cap_df = table_시총[0]

    # 1.3. 보통주 시가총액 추출
    market_cap_df_indexed = market_cap_df.set_index(market_cap_df.columns[0])
    sample_market_cap = float(market_cap_df_indexed.loc['시가총액(보통주,억원)'][1])
    # print('---시가총액 스크래핑 완료했습니다.---')
    # print(sample_market_cap)
    
    ##################################
    # 2. 최근 PER, PBR 수치 스크래핑 #
    ##################################
    # 2.1. PER, PBR 링크 파싱 
    per_pbr_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701'.format(code)
    html = requests.get(per_pbr_url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # 2.2. PER, PBR 포함된 메뉴항목 크롤링
    corp_group2 = soup.find_all(id='corp_group2')
    
    # 2.3. 계정명 탐색
    for acc_name in corp_group2:
        # 한글 계정명
        dt = acc_name.find_all('dt')
        # 숫자
        dd = acc_name.find_all('dd')
        
    # 2.4. 계정명 PER, PBR 인 항목의 숫자를 저장
    for idx, (t, d) in enumerate(zip(dt, dd)):
        if t.text.strip() == "PER(Price Earning Ratio)":
            sample_per.append(d.text.strip())
        elif t.text.strip().endswith('PBR(Price Book-value Ratio)'): 
            # print(idx, t.text.strip(), d.text.strip())
            sample_pbr.append(d.text.strip())

    """        
    ####################
    # 4. 딕셔너리 저장 #
    ####################
    try:
      self.finance_dict[code].update({'시가총액':sample_market_cap})
    except:
      self.finance_dict[code] = {'시가총액': sample_market_cap}
      print('--- 재무제표가 없어서 시가총액만 저장합니다. ---')

    print('---업데이트된 finance dict 입니다.----')
    print(self.finance_dict)  # 'A155660': {'매출액': 2343.0, '영업이익': 106.0, '지배주주순이익': 95.0, '영업현금흐름': 140.0, '시가총액': 726.0}, 'A001250': {'매출액': 40524.0, '영업이익': 569.0, '지배주주순이익': 187.0, '영업현금흐름': -100.0, '시가총액': 1680.0}}
    """
    
    market_cap[code] = sample_market_cap
    per[code] = sample_per
    pbr[code] = sample_pbr
    # print('---PER, PBR 스크래핑 완료했습니다.---')
    # print(sample_per, sample_pbr)
        
    return market_cap, pbr

  # 전종목 시가총액, pbr 추출
  def parsing_all_market_cap_PBR(self, code_list):
      all_market_cap_dict = {}
      all_per_dict = {}
      all_pbr_dict = {}
      
      # 전종목, 시가총액, PER, PBR 추출
      for idx, code in enumerate(code_list):
          print(idx, code)
          market_cap_one, pbr_one = self.get_market_cap_PBR(code)
          all_market_cap_dict.update(market_cap_one)
          # all_per_dict.update(per_one)
          all_pbr_dict.update(pbr_one)
      
      return all_market_cap_dict, all_pbr_dict


  # 데이터프레임화
  def gather_data_to_dataframe(self):
    #########################
    """6. 데이터프레임화"""
    #########################
    # 운영 재무 딕셔너리 읽기
    with open(self.filename_operating, 'rb') as f:
      finance_data = pickle.load(f)
    # finance_data = read_pickle(self.filename_operating)

    gpa = finance_data['gpa']
    ocf_a = finance_data['ocf_a']
    roic = finance_data['roic']
    op = finance_data['op']
    net_debt = finance_data['net_debt']
    finance_dict = finance_data['finance_dict']
    print('---운영용 재무 딕셔너리를 가져왔습니다.----')

    # 재무데이터 -> 데이터프레임화
    gpa_df = pd.DataFrame.from_dict(gpa, orient='index', columns=['gpa'])
    ocf_a_df = pd.DataFrame.from_dict(ocf_a, orient='index', columns=['ocf_a'])
    roic_df = pd.DataFrame.from_dict(roic, orient='index', columns=['roic'])
    op_df = pd.DataFrame.from_dict(op, orient='index', columns=['op'])
    net_debt_df = pd.DataFrame.from_dict(net_debt, orient='index', columns=['net_debt'])
    all_fin_dict = pd.DataFrame.from_dict(finance_dict, orient='index')

    # 벨류에이션 데이터 -> 데이터프레임화
    all_market_cap = pd.DataFrame.from_dict(self.all_market_cap, orient='index', columns=['market_cap'])
    print('---시총데이터프레임입니다.---')
    print(all_market_cap)
    # all_per = pd.DataFrame.from_dict(all_per, orient='index', columns=['per'])
    all_pbr = pd.DataFrame.from_dict(self.all_pbr, orient='index', columns=['pbr'])
    print('---pbr프레임입니다.---')
    print(all_pbr)

    # 데이터 붙이기 left join
    gpa_ocf_magic_df_all = pd.concat([gpa_df, ocf_a_df, roic_df, op_df, net_debt_df, all_fin_dict], axis=1, join='inner')
    value_df = pd.concat([all_market_cap, all_pbr], axis=1, join='inner')
    gpa_ocf_magic_value_all = pd.merge(gpa_ocf_magic_df_all, value_df, left_index=True, right_index=True, how='left')
    # gpa_ocf_magic_value_all.head()

    
    #########################
    # 3. PER, PCR, PSR 산출 #
    #########################
    # print("---finance dict입니다.---")
    # print(self.finance_dict)
    # per (시가총액 / 지배주주순이익)
    # gpa_ocf_magic_value_all['PER'] = gpa_ocf_magic_value_all['시가총액'] / gpa_ocf_magic_value_all['지배주주순이익']
    gpa_ocf_magic_value_all['PER'] = gpa_ocf_magic_value_all['market_cap'] / gpa_ocf_magic_value_all['당기순이익']
    gpa_ocf_magic_value_all['PSR'] = gpa_ocf_magic_value_all['market_cap'] / gpa_ocf_magic_value_all['매출액']
    gpa_ocf_magic_value_all['POR'] = gpa_ocf_magic_value_all['market_cap'] / gpa_ocf_magic_value_all['영업이익']
    gpa_ocf_magic_value_all['PCR'] = gpa_ocf_magic_value_all['market_cap'] / gpa_ocf_magic_value_all['영업현금흐름']
    print('==== 벨류에이션 수치 계산이 완료되었습니다.=====')
    print(gpa_ocf_magic_value_all.head())

    return gpa_ocf_magic_value_all

  # 업종코드 다운
  def get_krx_industry_code(self):
    #####################
    # STEP 01: Generate OTP
    #####################
    gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'

    # Form data
    gen_otp_data = {
        "name": "fileDown",
        "filetype": "xls",
        "url": "MKD/04/0406/04060100/mkd04060100_01",
        "market_gubun": "ALL",
        "isu_cdnm": "전체",
        "sort_type": "A",
        "lst_stk_vl": "1",
        "cpt": "1", 
        "isu_cdnm": "전체",
        "pagePath": "/contents/MKD/04/0406/04060100/MKD04060100.jsp"
        }

    # headers
    headers = {
        "Host": "marketdata.krx.co.kr",
        "Referer":"http://marketdata.krx.co.kr/mdi",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
        }
    
    # general
    r = requests.post(gen_otp_url, gen_otp_data, headers=headers)
    # otp 코드 획득
    code = r.content
    print(code)  # otp 코드 : h5UVIET8SHaPMfYQYgY27zGxpY99U2g45gttEVTLo

    #####################
    # STEP 02: download #
    #####################
    # general에서 정보확인
    down_url = "http://file.krx.co.kr/download.jspx"

    # form data 에서 정보확인
    down_data = {
        'code': code
        }
    # headers
    headers = {
        "Host": "file.krx.co.kr",
        "Origin": "http://marketdata.krx.co.kr",
        "Referer": "http://marketdata.krx.co.kr/mdi",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }

    # general :general에 게시된 url에서 formdata와 headers 형식으로 데이터를 요청해서 가져옴
    r = requests.post(down_url, down_data, headers=headers)
    print("r: ", r.content[0:6])  # 바이트배열 :  b'\xd0\xcf\x11\xe0\xa1\xb1'

    # io.BytesIO : 바이트배열을 이진파일로 다룰 수 있게 해주는 클래스
    f = io.BytesIO(r.content)
    print("*"*50)
    print("f: ", f) # f:  <_io.BytesIO object at 0x7f82dc361e08> 아잔파일로 전환됨
    print("*"*50)

    usecols = ['종목코드', '기업명', '업종코드', '업종']
    # 그냥 바이트배열은 읽기 어려움 -> io.BytesIO 로 이진배열 전환 -> read excel로 읽기
    df = pd.read_excel(f, converters={'종목코드': str, '업종코드': str}, usecols=usecols)
    print(df.head())
    df.columns = ['code', 'name', 'sector_code', 'sector']
    return df


  # 업종코드 붙이고 업종평균 계산
  def calculate_industry_average(self, industry_code_df, df):
    print('--- 샘플 업종코드 출력합니다. ---')
    print(industry_code_df.head())
    print('--- 샘플 데이터 출력합니다. ----')
    print(df.head())
    
    # 업종코드 수정 (종목코드, 기업명, 업종코드, 업종)
    print(type(industry_code_df))
    industry_code_df['code'] = 'A' + industry_code_df['code'].astype(str)
    print('--업종코드변경 성공!!--')
    print(industry_code_df.head())
    
    # 인덱스 변경
    print('--인덱스변경 완료---')
    industry_code_df = industry_code_df.set_index('code')
    
    # 결합
    df_2 = pd.merge(df, industry_code_df, left_index = True, right_index = True, how='left')
    print('df__2')
    print(df_2.head())

    # 업종평균 계산
    df_2 = self.caculate_average(df_2, 'pbr')
    df_2 = self.caculate_average(df_2, 'PER')
    df_2 = self.caculate_average(df_2, 'PCR')
    df_2 = self.caculate_average(df_2, 'PSR')
    df_2 = self.caculate_average(df_2, 'POR')

    return df_2

  # 결측치인 벨류에이션 값은 제거
  def caculate_average(self, df, col):
    df1 = df.copy()
    # PBR 특수문자값 제거
    lists = ['-','N/A',np.nan, np.inf,-np.inf,'','?','None','NaN','nan' ]
    df2 = df1.loc[df1[col].isin(lists) == False]  # 결측값이 아닌 것만 추출
    avg_col = 'industry_avg_' + str(col)
    df2[col] = df2[col].astype('float64')
    df2[avg_col] = df2[col].groupby(df2['sector_code']).transform('mean')

    return df2
  

  def make_magic_gpa_ocf_a_200_list(self, df):
    #####################################################################
    """7. 업종PER, 업종PBR, 업종PCR, 업종PSR 계산 후 200종목 내보내기"""
    #####################################################################
    # # 종목명 붙이기
    # code_name_df['종목코드'] = code_name_df['종목코드'].apply(lambda x : 'A' + str(x))
    # code_name_df = code_name_df.set_index('종목코드')
    # df = pd.merge(df,code_name_df, left_index=True, right_index=True, how='left')
    
    # # 회사명 앞으로
    # new_cols = ['회사명'] + [x for x in df.columns if '회사명' not in x]
    # print(new_cols)
    
    # df_new = df_new[new_cols]
    
    # 이익수익률 함수
    df_new = df.copy()
    df_new['earning_yields'] = df_new['op'].div(df_new['net_debt'] + df_new['market_cap'])
    # df.head()

    # 자본수익률, 이익수익률 순위산출
    df_new['roic_rank'] = df_new['roic'].rank(ascending=False)
    df_new['earning_yields_rank'] = df_new['earning_yields'].rank(ascending=False)

    # 마법공식 순위산출
    df_new['magic_point'] = df_new['roic_rank'] + df_new['earning_yields_rank']
    df_new['magic_rank'] = df_new['magic_point'].rank()

    # 마법공식 200종목 산출
    df_new = df_new.sort_values(['magic_rank'])
    # gpa_ocf_magic_value_all.head()
    magic_200_list = df_new.iloc[:200,:]
    
    # gpa_pbr list 200 추출
    df_new['gpa_rank'] = df_new['gpa'].rank(ascending=False)
    df_new['pbr_rank'] = df_new['pbr'].rank()
    df_new['gpa_pbr_point'] = df_new['gpa_rank'] + df_new['pbr_rank']
    df_new['gpa_pbr_rank'] = df_new['gpa_pbr_point'].rank()
    df_new = df_new.sort_values(['gpa_pbr_rank'])
    gpa_pbr_200_list = df_new.iloc[:200, :]
    
    # ocf_a_pbr list 200 추출
    df_new['ocf_a_rank'] = df_new['ocf_a'].rank(ascending=False)
    df_new['ocf_a_pbr_point'] = df_new['ocf_a_rank'] + df_new['pbr_rank']
    df_new['ocf_a_pbr_rank'] = df_new['ocf_a_pbr_point'].rank()
    df_new = df_new.sort_values(['ocf_a_pbr_rank'])
    ocf_a_pbr_200_list = df_new.iloc[:200, :]
    
    return magic_200_list, gpa_pbr_200_list, ocf_a_pbr_200_list, df_new

  

if __name__ == "__main__":
  # Quant 클래스인스턴스
  quant = QuantPick()
  # 재무 데이터 파싱
  path = '/content/drive/My Drive/stock/'
  filename = 'finance_data_for_operating.pkl'
  market_info_filename = 'market_cap_pbr_for_operating.pkl'

  if filename in os.listdir(path) :
    print('---운영 재무 딕셔너리가 존재합니다. 시가총액을 스크래핑합니다.---')
    gpa_ocf_magic_value_all_indust_avg = quant.run()

  else:
    print('---운영 재무 딕셔너리가 존재하지 않아, 재무정보를 스크래핑합니다.---')
    finance_data = quant.gather()
    # gpa, ocf_a, roic, op, net_debt, finance_dict= 
    # 시가총액 파싱 + 벨류에이션 및 업종 지표 산출
    gpa_ocf_magic_value_all_indust_avg = quant.run()

  # 200 리스트 피클, 엑셀저장
  magic_200_list, gpa_pbr_200_list, ocf_a_pbr_200_list, df_new = quant.final_200_list(gpa_ocf_magic_value_all_indust_avg)

  print("=========== Process completed!! ===========")
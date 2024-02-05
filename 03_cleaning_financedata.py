from getpass import getpass
from pymongo import MongoClient
import os
import pandas as pd


from pymongo import MongoClient
import pandas as pd


# MongoDB 연결
username = input("MongoDB 사용자 이름: ")
password = getpass("MongoDB 패스워드: ")  # 패스워드 안전하게 입력받기
MONGO_URI = f"mongodb://{username}:{password}@localhost:27017"
DATABASE_NAME = "stock_database"

# 클라이언트 생성
client = MongoClient(MONGO_URI)

# 데이터베이스 선택
financial_db = client[DATABASE_NAME]

# consolidated_financials 콜렉션 조회
consolidated_collection = financial_db['consolidated_financials']
consolidated_cursor = consolidated_collection.find()
consolidated_financials_df = pd.DataFrame(list(consolidated_cursor))

# individual_financials 콜렉션 조회
individual_collection = financial_db['individual_financials']
individual_cursor = individual_collection.find()
individual_financials_df = pd.DataFrame(list(individual_cursor))

# 결과 확인 (옵션)
print("Consolidated Financials:")
print(consolidated_financials_df.head())
print("\nIndividual Financials:")
print(individual_financials_df.head())

def cleaning_fin_data(df):
    df2 = df.copy()

    print(df2.columns.tolist())
    print('재무제표 종류값을 출력합니다.')
    print(df2['재무제표종류'].unique().tolist()[0].split(',')[0])
    fs_type_data = df2['재무제표종류'].unique().tolist()[0].split(',')[0]

    # 재무제표 유형 구분
    fs_type = ''
    if fs_type_data == '재무상태표':
        fs_type = 'bs'
    elif fs_type_data == '손익계산서':
        fs_type = 'is'
    elif fs_type_data == '현금흐름표':
        fs_type = 'cf'

    print('재무제표 유형을 출력합니다.')
    print(fs_type)

    return df2


print('재무제표 전처리를 시작합니다.')
# 전처리 실행 (현금흐름표, 연결)

consolidated_financials_df_cleaned = cleaning_fin_data(consolidated_financials_df)



################################################################################################
"""


# 재무제표 유형 구분
fs_type = ''
if '재무상태표' in filename:
    fs_type = 'bs'
elif '손익계산서' in filename:
    fs_type = 'is'
elif '현금흐름표' in filename:
    fs_type = 'cf'



# 의미 없는 컬럼 제거
for column in df.columns:
    if column.startswith('Unnamed'):
        del df[column]


# 여러 컬럼을 하나로 옮기기
column_transfer_map = {
    '당기 1분기': '당기',
    '당기 1분기 3개월': '당기',
    '당기 1분기말': '당기',
    '당기 반기': '당기',
    '당기 반기 3개월': '당기',
    '당기 반기말': '당기',
    '당기 반기 누적': '누적',
    '당기 3분기': '당기',
    '당기 3분기 3개월': '당기',
    '당기 3분기말': '당기',
    '당기 3분기 누적': '누적',
}

for column_from, column_to in column_transfer_map.items():
    if column_from in df:
        df.loc[~df[column_from].isnull(), column_to] = df.loc[~df[column_from].isnull(), column_from]
        del df[column_from]

# 항목명 선처리
df['항목명'] = df['항목명'].str.replace(' ', '', regex=False)
df['항목명'] = df['항목명'].str.replace('[^가-힣]+', '', regex=True)
df['항목명'] = df['항목명'].str.replace('\(\d+\)', '', regex=True)
df['항목명'] = df['항목명'].str.replace('\.$', '', regex=True)

# 항목명 일부 변경
item_partial_replace_map = {
    '(반)': '',
    '(분)': '',
    '(손실)': '',
    '(감소)': '',
    '(단위:원)': '',
    '으로인한': '',
    '지배기업소유주지분': '지배기업의소유주에게귀속되는자본',
    '수익(매출액)': '매출액',
    '영업수익': '매출액',
    '당기의순이익': '당기순이익',
    '반기순이익': '당기순이익',
    '분기순이익': '당기순이익',
}

if fs_type == 'cf':
    item_partial_replace_map.update({
        '순현금흐름': '현금흐름',
        '인한현금흐름': '현금흐름',
        '인한현금흐름': '현금흐름',
        '에서창출된현금흐름': '현금흐름',
    })

for str_from, str_to in item_partial_replace_map.items():
    df['항목명'] = df['항목명'].str.replace(str_from, str_to, regex=False)

# 항목명 전체 변경
item_entire_replace_map = {
    '매출': '매출액',
    '순이익': '당기순이익',
    '분기말자본': '자본총계',
    '기말자본': '자본총계',
    '자본의총계': '자본총계',
}

if fs_type == 'bs':
    item_entire_replace_map.update({
        '분기말': '자본총계',
        '기말': '자본총계',
        '보통주자본금': '자본금',
        '보통주': '자본금',
        '납입자본': '납입자본금',
    })
elif fs_type == 'is':
    item_entire_replace_map.update({
        '분기순이익': '당기순이익',
        '분기순손익': '당기순이익',
        '당기순손익': '당기순이익',
        '연결당기순이익': '당기순이익',
        '매출및지분법손익': '매출액',
        '수익순매출액': '매출액',
        '영업매출액': '매출액',
        '상품구입원가': '매출원가',
        '영업비용': '매출원가',
        '지배기업의소유주에게귀속되는자본': '당기순이익',
        '당기순이익순손실': '당기순이익',
        '매출액매출액': '매출액',
    })
elif fs_type == 'cf':
    item_entire_replace_map.update({
        '영업현금흐름': '영업활동현금흐름',
        '투자현금흐름': '투자활동현금흐름',
        '재무현금흐름': '재무활동현금흐름',
    })

for str_from, str_to in item_entire_replace_map.items():
    df.loc[df['항목명'] == str_from, '항목명'] = str_to

# 항목코드에 따른 항목명 변경
item_code_replace_map = {
    'ifrs-full_Revenue': '매출액',
    'ifrs-full_GrossProfit': '매출액',
    'ifrs-full_CostOfSales': '매출원가',
    'ifrs-full_ProfitLoss': '당기순이익',
    'dart_OperatingIncomeLoss': '영업이익',
    'ifrs-full_ProfitLossAttributableToOwnersOfParent': '당기순이익',
    'ifrs-full_CashFlowsFromUsedInOperatingActivities': '영업활동현금흐름',
    'ifrs-full_CashFlowsFromUsedInInvestingActivities': '투자활동현금흐름',
    'ifrs-full_CashFlowsFromUsedInFinancingActivities': '재무활동현금흐름',
}
for item_code, str_to in item_code_replace_map.items():
    df.loc[df['항목코드'] == item_code, '항목명'] = str_to

# 재무제표 유형에 따른 항목명 변경
if fs_type == 'bs':
    df.loc[df['항목명'].str.contains('기말') & df['항목명'].str.contains('잔액'), '항목명'] = '자본총계'
    df.loc[df['항목명'].str.endswith('기말자본'), '항목명'] = '자본총계'
    df.loc[df['항목명'].str.endswith('당분기말'), '항목명'] = '자본총계'
    df.loc[df['항목명'].str.endswith('당반기말'), '항목명'] = '자본총계'

df2 = df.dropna(subset=['당기'])
df2


df3 = df2[df2['항목명'].isin(['영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름'])][['회사명', '결산기준일', '보고서종류', '항목명', '당기']]
df3


# 테이블 pivot
df4 = df3.drop_duplicates(subset=['회사명', '항목명'])
df4 = df4.pivot(values='당기', index=['회사명', '결산기준일'], columns='항목명')
df4.columns.name = ''
df4 = df4.reset_index()
df4



# NaN 탐색
df4.loc[df4.isna().any(axis=1), :]


# 값 int로 치환
for column in ['영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름']:
    df4[column] = df4[column].apply(lambda x: int(x.replace(',', '')) if type(x) is str else x)




# 영업활동 +, 투자활동 -, 재무활동 -
mask1 = (df4['영업활동현금흐름'] > 0) & (df4['투자활동현금흐름'] < 0) & (df4['재무활동현금흐름'] < 0)
_df = df4[mask1]
_df.sort_values(by='영업활동현금흐름', ascending=False).iloc[:10]



# 영업활동 > 투자활동 + 재무활동
mask2 = df4['영업활동현금흐름'] > -(df4['투자활동현금흐름'] + df4['재무활동현금흐름'])
_df = df4[mask1 & mask2]
_df.sort_values(by='영업활동현금흐름', ascending=False).iloc[:10]


"""
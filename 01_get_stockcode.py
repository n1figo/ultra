from pymongo import MongoClient
from getpass import getpass
import pandas as pd



def get_stocks(market=None):
    market_type = ''
    if market == 'kospi':
        market_type = '&marketType=stockMkt'
    elif market == 'kosdaq':
        market_type = '&marketType=kosdaqMkt'
    elif market == 'konex':
        market_type = '&marketType=konexMkt'
        
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?currentPageSize=5000&pageIndex=1&method=download&searchType=13{market_type}'.format(market_type=market_type)

    list_df_stocks = pd.read_html(url, header=0, converters={'종목코드': lambda x: str(x)})
    df_stocks = list_df_stocks[0]
    return df_stocks

kospi_df = get_stocks('kospi')
kosdaq_df = get_stocks('kosdaq')
# df = get_stocks('kosdaq')

# print(df.head())



# 데이터프레임 예시 (주식 종목 코드와 관련 정보)
data = {
    'stock_code': ['0001', '0002', '0003'],
    'company_name': ['Company A', 'Company B', 'Company C'],
    'price': [100, 200, 150]
}
df = pd.DataFrame(data)


"""2. mongodb업로드"""

# kospi_df = pd.DataFrame(kospi_data)
# kosdaq_df = pd.DataFrame(kosdaq_data)

# MongoDB 연결 정보
username = input("MongoDB 사용자 이름: ")
password = getpass("MongoDB 패스워드: ")  # 패스워드 안전하게 입력받기
MONGO_URI = f"mongodb://{username}:{password}@localhost:27017"
DATABASE_NAME = "stock_database"
KOSPI_COLLECTION_NAME = "kospi_stock_codes"
KOSDAQ_COLLECTION_NAME = "kosdaq_stock_codes"

# 클라이언트 생성
client = MongoClient(MONGO_URI)

# 데이터베이스 선택
db = client[DATABASE_NAME]

# 코스피 컬렉션 선택 및 데이터 삽입
kospi_collection = db[KOSPI_COLLECTION_NAME]
kospi_records = kospi_df.to_dict(orient='records')
kospi_collection.insert_many(kospi_records)

# 코스닥 컬렉션 선택 및 데이터 삽입
kosdaq_collection = db[KOSDAQ_COLLECTION_NAME]
kosdaq_records = kosdaq_df.to_dict(orient='records')
kosdaq_collection.insert_many(kosdaq_records)

print("데이터 업로드 완료!")


# # MongoDB 연결 정보
# username = input("MongoDB 사용자 이름: ")
# password = getpass("MongoDB 패스워드: ")  # 패스워드 안전하게 입력받기
# MONGO_URI = f"mongodb://{username}:{password}@localhost:27017"
# DATABASE_NAME = "stock_database"
# COLLECTION_NAME = "stock_codes"

# # 클라이언트 생성
# client = MongoClient(MONGO_URI)

# # 데이터베이스 선택
# db = client[DATABASE_NAME]

# # 컬렉션 선택
# collection = db[COLLECTION_NAME]

# # 데이터프레임을 딕셔너리 리스트로 변환
# records = df.to_dict(orient='records')

# # MongoDB에 삽입
# collection.insert_many(records)

# print("데이터 업로드 완료!")

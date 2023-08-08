from pymongo import MongoClient, UpdateOne

# MongoDB 연결 정보
MONGO_URI = "mongodb://admin:dnsehd10djr!@localhost:27017"  # 여기에 관리자 계정의 사용자 이름과 비밀번호를 입력하세요
DATABASE_NAME = "your_database"  # 사용할 데이터베이스 이름
COLLECTION_NAME = "your_collection"  # 인덱스를 생성할 컬렉션 이름

# 클라이언트 생성
client = MongoClient(MONGO_URI)

# 데이터베이스 선택
db = client[DATABASE_NAME]

# 컬렉션 선택
coll = db[COLLECTION_NAME]

# 인덱스 생성 (예: 'field_name' 필드에 대한 오름차순 인덱스)
coll.create_index("field_name")




# 조회 비용을 절약하기 위하여 인덱스 생성
import pymongo

# coll.create_index( [ ( 'code', pymongo.ASCENDING ), ( 'date', pymongo.DESCENDING ) ], unique=True )
coll.create_index( [ ( 'code', pymongo.ASCENDING ) ] )
coll.create_index( [ ( 'date', pymongo.DESCENDING ) ] )


print("인덱스 생성 완료!")

# 데이터 삽입 및 조회하기 
reqs = []
item = {'code': '005930', 'date': '20220707', 'close': 58200, 'diff': 1800, 'diffratio': 3.1914893617021276, 'high': 58700, 'low': 56300, 'open': 56400, 'price': 1217857000000, 'volume': 21034193}
reqs.append(UpdateOne({'code': item['code'], 'date': item.get('date')}, {'$set': item}, upsert=True))


# # UpdateOne을 사용한 예시
# updates = [
#     UpdateOne({"_id": 1}, {"$set": {"field": "value"}}),
#     UpdateOne({"_id": 2}, {"$set": {"field": "another_value"}}),
# ]

# collection.bulk_write(updates)

# 추가할 item을 위와 같이 UpdateOne으로 reqs에 추가
coll.bulk_write(reqs, ordered=False)


# 삽입한 데이터를 dict의 리스트로 가져오기
cursor = coll.find({}, {'_id': 0})  # 전체 데이터 조회
cursor = coll.find({'code': '005930'}, {'_id': 0}, sort=[('date', 1)])  # 삼성전자 조회 (date 오름차순)
cursor = coll.find({'date': '20220707'}, {'_id': 0})  # 특정 날짜 조회

data = list(cursor)  # dict의 list로 가져오기

import pandas as pd
df = pd.DataFrame(data)  # Pandas DataFrame으로 변환

print(df.head())

print("테이터 삽입 및 조회완료!")


"""


# 생성한 client로 database와 collection 생성
db = client.findata
coll = db.stock_candles









# 데이터 삽입 및 조회하기 
reqs = []
item = {'code': '005930', 'date': '20220707', 'close': 58200, 'diff': 1800, 'diffratio': 3.1914893617021276, 'high': 58700, 'low': 56300, 'open': 56400, 'price': 1217857000000, 'volume': 21034193}
reqs.append(UpdateOne({'code': code, 'date': item.get('date')}, {'$set': item}, upsert=True))
// 추가할 item을 위와 같이 UpdateOne으로 reqs에 추가
coll.bulk_write(reqs, ordered=False)


# 삽입한 데이터를 dict의 리스트로 가져오기
cursor = coll.find({}, {'_id': 0})  # 전체 데이터 조회
cursor = coll.find({'code': '005930'}, {'_id': 0}, sort=[('date', 1)])  # 삼성전자 조회 (date 오름차순)
cursor = coll.find({'date': '20220707'}, {'_id': 0})  # 특정 날짜 조회
...
data = list(cursor)  # dict의 list로 가져오기

import pandas as pd
df = pd.DataFrame(data)  # Pandas DataFrame으로 변환

"""
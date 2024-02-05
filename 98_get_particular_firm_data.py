import dart_fss as dart
import ssl

context = ssl._create_unverified_context()
res = urlopen()

# Open DART API KEY 설정
api_key='647ca5d9c52a0d3b63b636760f1c5cdcf97ebfe1'
dart.set_api_key(api_key=api_key)


# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

# 삼성전자 검색
samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]

# 2012년부터 연간 연결재무제표 불러오기
fs = samsung.extract_fs(bgn_de='20120101')

# 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
fs.save()

"""
############################
# 현재 날짜 불러오기
now = datetime.datetime.now()
nowDate = now.strftime('%Y%m%d%H%M')
# 검색 시작 날짜
bgn_de = '20190101'
# 검색 종료 날짜
end_de = now.strftime('%Y%m%d')

# 모든 상장된 기업 리스트 불러오기
corp_list = dart.get_corp_list()

# 원하는 기업이름 입력
corp_name = '삼성전자'
corp_code = corp_list.find_by_corp_name(corp_name=corp_name)[0]
corp_code = corp_code._info['corp_code']

# 2019년 01월 01일에 올라온 연결재무제표부터 현재까지 검색
# 사업 보고서
# fs = dart.fs.extract(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de, lang='ko', separator=False)
# 반기 보고서 [report_tp='half']
# fs = dart.fs.extract(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de, report_tp='half', lang='ko', separator=False)
# 분기 보고서 [report_tp='quarter']
fs = dart.fs.extract(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de, report_tp='quarter', lang='ko', separator=False)

# 재무제표 일괄저장 (default: 실행폴더/fsdata/{corp_code}_{report_tp}.xlsx)
filename = corp_name + '_' + nowDate + '.xlsx'
# path = 'C:/Users/User/hb_jeong/Desktop/'
fs.save(filename=filename)

"""
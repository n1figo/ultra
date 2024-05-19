import pandas as pd
import os


input_filename_folder = os.path.join('/workspaces/ultra/input/240517134606_퀀트데이터2024.05.17(24년1Q 실적데이터반영).xlsx.xlsx')
data = pd.read_excel(input_filename_folder, header=1)
# print(data.head())

# 데이터채우기
data['업종소'] = data['업종소'].fillna(data['업종대'])

# Verify and filter data to ensure there are no missing values in 'Industry' and 'ROE' columns
filtered_data = data.dropna(subset=['업종소', 'ROA (%)'])

# Assuming 'ROE' needs to be converted to numeric type if it's not already
filtered_data['ROA (%)'] = pd.to_numeric(filtered_data['ROA (%)'], errors='coerce')

# Remove any rows that couldn't be converted to numbers (if necessary)
filtered_data = filtered_data.dropna(subset=['ROA (%)'])

# Group by 'Industry' and select the top two companies based on 'ROE'
top_companies_by_industry = filtered_data.groupby('업종소').apply(lambda x: x.nlargest(2, 'ROA (%)')).reset_index(drop=True)

# Display the top companies
print(top_companies_by_industry)

top_companies_by_industry.to_csv('/workspaces/ultra/output/업종상위ROAtop2.csv', encoding='cp949')
print('추출작업완료!')


# import streamlit as st
# import requests
# import pandas as pd
# import os

# # 환경 변수에서 API 키 가져오기
# api_key = os.getenv('API_KEY')

# # DART에 요청을 보내 데이터 가져오기
# def get_company_data():
#     url = f"https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}&page_no=1&bgn_de=20230101&end_de=20231231&pblntf_ty=A"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         return pd.DataFrame(data['list'])
#     else:
#         st.error(f"API 요청에 실패했습니다: {response.status_code}, {response.text}")
#         return pd.DataFrame()

# # 데이터 처리 및 ROE 계산
# def analyze_data(df):
#     df = df[['corp_name', 'sector_wics', 'roe']]
#     result = df.groupby('sector_wics').apply(lambda x: x.nlargest(2, 'roe'))
#     return result.reset_index(drop=True)

# # Streamlit 인터페이스 설정
# def main():
#     st.title('DART WICS 업종별 ROE 1위 및 2위 회사')

#     if st.button('데이터 가져오기'):
#         df = get_company_data()
#         if not df.empty:
#             st.success("데이터를 성공적으로 가져왔습니다!")
#             result = analyze_data(df)
#             st.write(result)
#         else:
#             st.error("데이터를 가져오는 데 실패했습니다. API 키를 확인하거나 요청 파라미터를 조정해주세요.")

# if __name__ == "__main__":
#     main()




# # import streamlit as st
# # import requests
# # import pandas as pd
# # import os  # 환경 변수를 가져오기 위한 모듈 추가

# # # 환경 변수에서 API 키 가져오기
# # api_key = os.getenv('API_KEY')  # API 키를 환경 변수에서 불러오기

# # # DART에 요청을 보내 데이터 가져오기
# # def get_company_data():
# #     url = f"https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}&page_no=1&bgn_de=20230101&end_de=20231231&pblntf_ty=A"
# #     response = requests.get(url)
# #     data = response.json()
# #     return pd.DataFrame(data['list'])

# # # 데이터 처리 및 ROE 계산
# # def analyze_data(df):
# #     # 데이터 프레임에서 필요한 업종 정보와 ROE 정보 추출
# #     df = df[['corp_name', 'sector_wics', 'roe']]
# #     # 업종별로 그룹화하고, ROE 기준으로 정렬하여 상위 2개 회사 선택
# #     result = df.groupby('sector_wics').apply(lambda x: x.nlargest(2, 'roe'))
# #     return result.reset_index(drop=True)

# # # Streamlit 인터페이스 설정
# # def main():
# #     st.title('DART WICS 업종별 ROE 1위 및 2위 회사')

# #     if st.button('데이터 가져오기'):
# #         df = get_company_data()
# #         if not df.empty:
# #             st.success("데이터를 성공적으로 가져왔습니다!")
# #             result = analyze_data(df)
# #             st.write(result)
# #         else:
# #             st.error("데이터를 가져오는 데 실패했습니다. API 키를 확인하거나 요청 파라미터를 조정해주세요.")

# # if __name__ == "__main__":
# #     main()



# # import streamlit as st
# # import requests
# # import pandas as pd

# # # API 키 설정
# # api_key = 'your_api_key_here'

# # # DART에 요청을 보내 데이터 가져오기
# # def get_company_data():
# #     url = f"https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}&page_no=1&bgn_de=20230101&end_de=20231231&pblntf_ty=A"
# #     response = requests.get(url)
# #     data = response.json()
# #     return pd.DataFrame(data['list'])

# # # 데이터 처리 및 ROE 계산
# # def analyze_data(df):
# #     # 데이터 프레임에서 필요한 업종 정보와 ROE 정보 추출
# #     # 예시로, 업종과 ROE 컬럼을 선택 (실제 데이터에 맞게 조정 필요)
# #     df = df[['corp_name', 'sector_wics', 'roe']]
# #     # 업종별로 그룹화하고, ROE 기준으로 정렬하여 상위 2개 회사 선택
# #     result = df.groupby('sector_wics').apply(lambda x: x.nlargest(2, 'roe'))
# #     return result.reset_index(drop=True)

# # # Streamlit 인터페이스 설정
# # def main():
# #     st.title('DART WICS 업종별 ROE 1위 및 2위 회사')

# #     if st.button('데이터 가져오기'):
# #         df = get_company_data()
# #         if not df.empty:
# #             st.success("데이터를 성공적으로 가져왔습니다!")
# #             result = analyze_data(df)
# #             st.write(result)
# #         else:
# #             st.error("데이터를 가져오는 데 실패했습니다. API 키를 확인하거나 요청 파라미터를 조정해주세요.")

# # if __name__ == "__main__":
# #     main()
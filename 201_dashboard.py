import streamlit as st
import pandas as pd

# 제목 설정
st.set_page_config(page_title="CSV 파일 대시보드")

# CSV 파일 경로
csv_file_path = "/workspaces/ultra/output/20240408_울트라_normal.csv"

# CSV 파일 읽기
df = pd.read_csv(csv_file_path, encoding='cp949')

# CSV 파일 데이터 표시
st.write("CSV 파일 데이터:")
st.write(df)

# 데이터 시각화
st.subheader("데이터 시각화")
# 여기에 시각화 코드를 추가하세요. 예: st.line_chart(df['열이름'])
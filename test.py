import pandas as pd
import numpy as np


df = pd.read_csv('./output/울트라_normal.csv', encoding='cp949')
# print(df.head())

for col in df.columns.tolist():
    if 'F' in col:
        print(col)


print(df['F스코어 지배주주순익>0 여부'].value_counts())
print(df['F스코어 영업활동현금흐름>0 여부'].value_counts())
print(df['F스코어 신주발행X 여부'].value_counts())

#### test
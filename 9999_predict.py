
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_absolute_error

# 데이터 읽기
# path = 'C:/Users/kbins/Downloads/240508_2.csv'
path = '/workspace/ULTRA/input/240508_2.csv'
data = pd.read_csv(path, sep=',', encoding='cp949')

# 칼럼명의 공백 제거
data.columns = [col.replace(" ", "") for col in data.columns]

# 데이터 타입 오류 수정: 모든 수치 데이터를 숫자형으로 변환
for col in data.columns:
    if data[col].dtype == object:
        data[col] = pd.to_numeric(data[col].apply(lambda x: x.replace(" ", "")), errors='coerce')

# '연월' 컬럼을 datetime 형식으로 변환
data['연월'] = pd.to_datetime(data['연월'].astype(str), format='%Y%m')

# 데이터를 시간 순으로 정렬
data.sort_values(by='연월', inplace=True)

# MAU 데이터를 추출
mau_data = data[['MAU']].values

# 데이터 정규화
scaler = MinMaxScaler(feature_range=(0, 1))
mau_scaled = scaler.fit_transform(mau_data)

# 데이터셋 생성 함수
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# 데이터셋 생성
look_back = 3
X, y = create_dataset(mau_scaled, look_back)

# 데이터를 훈련 세트와 테스트 세트로 분할
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 입력을 [samples, time steps, features]로 reshape
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# LSTM 모델 구축
model = Sequential()
model.add(LSTM(50, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2)

# 예측 수행
y_pred = model.predict(X_test)

# 예측 결과 역정규화
y_pred_inverse = scaler.inverse_transform(y_pred)
y_test_inverse = scaler.inverse_transform([y_test])

# 예측 성능 평가
mae = mean_absolute_error(y_test_inverse[0], y_pred_inverse[:,0])
print(f"MAE: {mae:.2f}")

# 실제값과 예측값 출력
results_df = pd.DataFrame({
    'Actual MAU': y_test_inverse[0],
    'Predicted MAU': y_pred_inverse[:,0]
})
print(results_df)

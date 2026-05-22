# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# CSV 읽기
# -----------------------------
try:
    df = pd.read_csv("populationssss.csv", encoding="cp949")
except:
    df = pd.read_csv("populationssss.csv", encoding="euc-kr")

# -----------------------------
# 데이터 전처리
# -----------------------------
df = df.dropna(axis=1, how='all')

# 첫 번째 열 이름 변경
df.rename(columns={df.columns[0]: '행정구'}, inplace=True)

# 숫자형 변환
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# -----------------------------
# 제목
# -----------------------------
st.title("서울시의 인구통계")

# -----------------------------
# 행정구 선택
# -----------------------------
district = st.selectbox(
    "행정구를 선택하세요",
    df['행정구']
)

selected = df[df['행정구'] == district]

# 연령대 / 인구수
ages = df.columns[1:]
population = selected.iloc[0, 1:]

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# 배경색
fig.patch.set_facecolor('#E6E6FA')
ax.set_facecolor('#E6E6FA')

# 그래프
ax.plot(
    ages,
    population,
    color='red',
    marker='o',
    linewidth=2
)

# 제목
ax.set_title("서울시의 인구통계", fontsize=18)

# 축 이름
ax.set_xlabel("연령대")
ax.set_ylabel("인구수")

# x축 회전
plt.xticks(rotation=45)

# 출력
st.pyplot(fig)

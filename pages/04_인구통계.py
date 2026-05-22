# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 데이터 불러오기
# -----------------------------
df = pd.read_csv("populationssss.csv", encoding="utf-8")

# 필요 없는 열 제거
if '10~19세' in df.columns:
    try:
        df['10~19세'] = pd.to_numeric(df['10~19세'], errors='coerce')
    except:
        pass

# 숫자형 변환
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# -----------------------------
# Streamlit 제목
# -----------------------------
st.title("서울시의 인구통계")

# -----------------------------
# 행정구 선택
# -----------------------------
district = st.selectbox(
    "행정구를 선택하세요",
    df.iloc[:, 0]
)

# 선택 데이터 추출
selected = df[df.iloc[:, 0] == district]

# 연령대 / 인구수
ages = df.columns[1:]
population = selected.iloc[0, 1:]

# -----------------------------
# 그래프 생성
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 5))

# 배경색
fig.patch.set_facecolor('#E6E6FA')
ax.set_facecolor('#E6E6FA')

# 꺾은선 그래프
ax.plot(
    ages,
    population,
    color='red',
    marker='o',
    linewidth=2
)

# 제목 및 축 이름
ax.set_title("서울시의 인구통계", fontsize=16)
ax.set_xlabel("연령대")
ax.set_ylabel("인구수")

# x축 글자 회전
plt.xticks(rotation=45)

# 출력
st.pyplot(fig)

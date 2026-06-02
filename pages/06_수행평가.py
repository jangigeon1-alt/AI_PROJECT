import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="AI 관광지 추천 시스템",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ AI 관광지 최적 여행 시기 추천 시스템")

st.write(
    "월과 여행 스타일을 선택하면 가장 적합한 관광지를 추천합니다."
)

# --------------------------------
# 데이터 불러오기
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("tourist_spots.csv")

df = load_data()

# --------------------------------
# 입력
# --------------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox(
        "📅 여행 월",
        range(1, 13)
    )

with col2:
    style = st.selectbox(
        "🎯 여행 스타일",
        [
            "전체",
            "역사탐방",
            "자연경관",
            "액티비티",
            "휴양"
        ]
    )

# --------------------------------
# 추천 관광지 추출
# --------------------------------
recommended = df[
    df["추천월"].astype(str).str.contains(
        str(month),
        na=False
    )
].copy()

# --------------------------------
# 결과 없을 때
# --------------------------------
if recommended.empty:

    st.warning(
        f"{month}월에 등록된 추천 관광지가 없습니다."
    )

    st.info(
        "현재 데이터 기준으로는 추천 가능한 관광지가 없습니다."
    )

    st.stop()

# --------------------------------
# AI 점수 계산
# --------------------------------
recommended["추천점수"] = 70

if style != "전체":

    recommended.loc[
        recommended["스타일"] == style,
        "추천점수"
    ] += 30

# 대표 관광지 가산점
popular_spots = [
    "경복궁",
    "불국사",
    "성산일출봉",
    "해운대",
    "남이섬"
]

recommended.loc[
    recommended["관광지"].isin(popular_spots),
    "추천점수"
] += 5

recommended = recommended.sort_values(
    by="추천점수",
    ascending=False
)

# --------------------------------
# 추천 TOP5
# --------------------------------
st.subheader("🌟 추천 관광지 TOP 5")

for _, row in recommended.head(5).iterrows():

    st.markdown(
        f"""
### 📍 {row['관광지']}

⭐ 추천점수 : {row['추천점수']}점

🏷️ 여행스타일 : {row['스타일']}

💡 추천이유 : {row['추천이유']}
"""
    )

# --------------------------------
# 지도
# --------------------------------
st.subheader("🗺️ 관광지 위치")

fig = px.scatter_map(
    recommended,
    lat="위도",
    lon="경도",
    hover_name="관광지",
    hover_data=["지역"],
    zoom=5,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# 상세정보
# --------------------------------
st.subheader("📍 관광지 상세 정보")

selected = st.selectbox(
    "관광지 선택",
    recommended["관광지"].tolist()
)

info = recommended[
    recommended["관광지"] == selected
]

if not info.empty:

    info = info.iloc[0]

    st.write(f"### {info['관광지']}")
    st.write(f"📌 지역 : {info['지역']}")
    st.write(f"🏷️ 스타일 : {info['스타일']}")
    st.write(f"📅 추천월 : {info['추천월']}")
    st.write(f"⭐ 추천점수 : {info['추천점수']}점")
    st.write(f"💡 추천이유 : {info['추천이유']}")

# --------------------------------
# 데이터 보기
# --------------------------------
with st.expander("📊 추천 관광지 데이터"):

    st.dataframe(
        recommended[
            [
                "관광지",
                "지역",
                "스타일",
                "추천월",
                "추천점수"
            ]
        ],
        use_container_width=True
    )

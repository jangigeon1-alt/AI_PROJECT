import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="AI 관광지 추천 시스템",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ AI 관광지 최적 여행 시기 추천 시스템")

st.markdown("""
사용자의 여행 월과 여행 스타일을 분석하여
최적의 관광지를 추천합니다.
""")

# ----------------------------
# 데이터 불러오기
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("tourist_spots.csv")

df = load_data()

# ----------------------------
# 입력
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox(
        "📅 여행 월 선택",
        range(1, 13)
    )

with col2:
    style = st.selectbox(
        "🎯 여행 스타일 선택",
        ["전체", "역사탐방", "자연경관", "액티비티", "휴양"]
    )

# ----------------------------
# 추천월 문자열 변환
# ----------------------------
df["추천월"] = df["추천월"].astype(str)

# ----------------------------
# 월 기준 필터링
# ----------------------------
recommended = df[
    df["추천월"].str.contains(
        str(month),
        na=False
    )
].copy()

# ----------------------------
# AI 점수 계산
# ----------------------------
if not recommended.empty:

    recommended["추천점수"] = 50

    if style != "전체":

        recommended.loc[
            recommended["스타일"] == style,
            "추천점수"
        ] += 50

    popular_spots = [
        "경복궁",
        "남이섬",
        "성산일출봉",
        "불국사",
        "해운대"
    ]

    recommended.loc[
        recommended["관광지"].isin(popular_spots),
        "추천점수"
    ] += 10

    recommended = recommended.sort_values(
        by="추천점수",
        ascending=False
    )

# ----------------------------
# 결과 없음
# ----------------------------
if recommended.empty:

    st.warning(
        "선택한 조건에 맞는 관광지가 없습니다."
    )

# ----------------------------
# 결과 있음
# ----------------------------
else:

    st.subheader(
        f"🌟 {month}월 추천 관광지 TOP 5"
    )

    top5 = recommended.head(5)

    for _, row in top5.iterrows():

        st.markdown(
            f"""
### 📍 {row['관광지']}

⭐ 추천점수 : {row['추천점수']}점

🏷️ 스타일 : {row['스타일']}

💡 {row['추천이유']}
---
"""
        )

    # ----------------------------
    # 지도
    # ----------------------------
    st.subheader("🗺️ 관광지 지도")

    fig = px.scatter_map(
        recommended,
        lat="위도",
        lon="경도",
        hover_name="관광지",
        hover_data=[
            "지역",
            "스타일",
            "추천점수"
        ],
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

    # ----------------------------
    # 상세 정보
    # ----------------------------
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

    # ----------------------------
    # 데이터표
    # ----------------------------
    with st.expander("📊 전체 데이터 보기"):

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

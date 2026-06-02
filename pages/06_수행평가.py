import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI 관광지 추천 시스템",
    layout="wide"
)

st.title("🗺️ AI 관광지 최적 여행 시기 추천")

df = pd.read_csv("tourist_spots.csv")

month = st.selectbox(
    "📅 여행 월 선택",
    range(1,13)
)

# 추천 관광지 추출
recommended = df[
    df["추천월"].str.contains(str(month))
].copy()

# 점수 계산
recommended["추천점수"] = 100

st.subheader(f"🌟 {month}월 추천 관광지")

if len(recommended) > 0:

    recommended = recommended.sort_values(
        "추천점수",
        ascending=False
    )

    st.dataframe(
        recommended[
            ["관광지","지역","추천이유"]
        ],
        use_container_width=True
    )

    # 지도
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

    selected = st.selectbox(
        "📍 관광지 선택",
        recommended["관광지"]
    )

    info = recommended[
        recommended["관광지"] == selected
    ].iloc[0]

    st.markdown("## 관광지 정보")

    st.write(f"관광지 : {info['관광지']}")
    st.write(f"지역 : {info['지역']}")
    st.write(f"추천월 : {info['추천월']}")
    st.write(f"추천이유 : {info['추천이유']}")

else:
    st.warning("추천 관광지가 없습니다.")

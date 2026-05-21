import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="🌍 MBTI 세계 분석",
    page_icon="🌎",
    layout="wide"
)

# -----------------------------------
# 스타일
# -----------------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    font-weight: 800;
}

.stSelectbox label {
    font-size: 20px;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    font-size: 38px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

country_col = df.columns[0]
mbti_cols = df.columns[1:]

# -----------------------------------
# 타이틀
# -----------------------------------
st.title("🌍 국가별 MBTI 인터랙티브 분석")
st.caption("Plotly 기반 인터랙티브 시각화 😼")

# -----------------------------------
# 사이드바
# -----------------------------------
st.sidebar.header("⚙️ 설정")

country = st.sidebar.selectbox(
    "국가 선택",
    sorted(df[country_col].unique())
)

# -----------------------------------
# 선택 국가 데이터
# -----------------------------------
selected = df[df[country_col] == country]

mbti_values = selected.iloc[0, 1:]

chart_df = pd.DataFrame({
    "MBTI": mbti_values.index,
    "비율": mbti_values.values
})

chart_df = chart_df.sort_values(
    by="비율",
    ascending=False
)

# -----------------------------------
# 1등 MBTI 찾기
# -----------------------------------
top_mbti = chart_df.iloc[0]["MBTI"]
top_value = chart_df.iloc[0]["비율"]

# -----------------------------------
# 색상 설정
# -----------------------------------
colors = []

blue_gradient = px.colors.sequential.Blues[::-1]

for i in range(len(chart_df)):
    if i == 0:
        colors.append("#ff2b2b")  # 빨간색
    else:
        colors.append(
            blue_gradient[min(i, len(blue_gradient)-1)]
        )

# -----------------------------------
# 대표 MBTI 카드
# -----------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🔥 대표 MBTI",
        top_mbti
    )

with col2:
    st.metric(
        "📈 비율",
        f"{top_value:.1%}"
    )

# -----------------------------------
# Plotly 막대그래프
# -----------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["MBTI"],
        y=chart_df["비율"],
        marker_color=colors,
        text=[
            f"{v:.1%}" for v in chart_df["비율"]
        ],
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.1%}<extra></extra>"
    )
)

fig.update_layout(
    title=f"📊 {country} MBTI 비율",
    template="plotly_dark",
    height=650,
    xaxis_title="MBTI",
    yaxis_title="비율",
    hovermode="x",
    font=dict(
        size=16
    ),
    title_font=dict(
        size=28
    ),
    xaxis=dict(
        tickfont=dict(size=15)
    ),
    yaxis=dict(
        tickformat=".0%",
        gridcolor="rgba(255,255,255,0.08)"
    ),
    margin=dict(
        t=90,
        l=40,
        r=30,
        b=40
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# 전체 평균 MBTI
# -----------------------------------
st.markdown("---")

st.subheader("🌎 전 세계 평균 MBTI TOP 5")

mean_values = (
    df.iloc[:, 1:]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

avg_df = pd.DataFrame({
    "MBTI": mean_values.index,
    "평균 비율": mean_values.values
})

fig2 = px.pie(
    avg_df,
    names="MBTI",
    values="평균 비율",
    hole=0.45
)

fig2.update_layout(
    template="plotly_dark",
    height=500,
    title="🔥 세계 평균 MBTI 비율"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# 데이터 테이블
# -----------------------------------
with st.expander("📋 전체 데이터 보기"):
    st.dataframe(
        df,
        use_container_width=True
    )

# -----------------------------------
# 푸터
# -----------------------------------
st.markdown("---")
st.caption("😼 Streamlit + Plotly Dashboard")

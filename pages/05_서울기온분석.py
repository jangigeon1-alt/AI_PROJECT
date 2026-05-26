import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ----------------------------
# 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="날짜별 기온분석",
    layout="wide"
)

st.title("📈 날짜별 기온분석")

st.write("CSV 파일을 업로드해주세요.")

# ----------------------------
# 파일 업로드
# ----------------------------
uploaded_file = st.file_uploader(
    "seoul.csv 업로드",
    type=["csv"]
)

# ----------------------------
# 파일 업로드 전
# ----------------------------
if uploaded_file is None:
    st.info("CSV 파일을 업로드하면 그래프가 표시됩니다.")

# ----------------------------
# 파일 업로드 후
# ----------------------------
else:

    @st.cache_data
    def load_data(file):

        # CSV 읽기
        df = pd.read_csv(file, encoding="cp949")

        # 컬럼 공백 제거
        df.columns = df.columns.str.strip()

        # 날짜 변환
        df['날짜'] = pd.to_datetime(df['날짜'])

        # 연/월/일 컬럼 생성
        df['연도'] = df['날짜'].dt.year
        df['월'] = df['날짜'].dt.month
        df['일'] = df['날짜'].dt.day

        return df

    df = load_data(uploaded_file)

    # ----------------------------
    # 월/일 선택
    # ----------------------------
    col1, col2 = st.columns(2)

    with col1:
        month = st.selectbox(
            "월 선택",
            range(1, 13)
        )

    with col2:
        day = st.selectbox(
            "일 선택",
            range(1, 32)
        )

    # ----------------------------
    # 데이터 필터링
    # ----------------------------
    filtered = df[
        (df['월'] == month) &
        (df['일'] == day)
    ].sort_values('연도')

    # ----------------------------
    # 데이터 없을 때
    # ----------------------------
    if filtered.empty:
        st.warning("해당 날짜 데이터가 없습니다.")

    else:

        # ----------------------------
        # 그래프 생성
        # ----------------------------
        fig = go.Figure()

        # 최고기온
        fig.add_trace(
            go.Scatter(
                x=filtered['연도'],
                y=filtered['최고기온(℃)'],
                mode='lines+markers',
                name='최고기온',
                line=dict(
                    color='hotpink',
                    width=3
                ),
                marker=dict(size=6)
            )
        )

        # 최저기온
        fig.add_trace(
            go.Scatter(
                x=filtered['연도'],
                y=filtered['최저기온(℃)'],
                mode='lines+markers',
                name='최저기온',
                line=dict(
                    color='lightblue',
                    width=3
                ),
                marker=dict(size=6)
            )
        )

        # ----------------------------
        # 레이아웃 설정
        # ----------------------------
        fig.update_layout(
            title='날짜별 기온분석',
            xaxis_title='연도',
            yaxis_title='온도 (℃)',
            legend_title='범례',
            template='plotly_white',
            hovermode='x unified',
            height=650
        )

        # 그래프 출력
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------
        # 데이터 표
        # ----------------------------
        st.subheader("📋 데이터 표")

        st.dataframe(
            filtered[
                [
                    '연도',
                    '최고기온(℃)',
                    '최저기온(℃)'
                ]
            ],
            use_container_width=True
        )

import streamlit as st
import random

st.set_page_config(
    page_title="MBTI 진로 추천기 😎",
    page_icon="🔥",
    layout="centered"
)

# MBTI별 진로 데이터
career_data = {
    "INTJ": [
        {
            "career": "🧠 AI 개발자",
            "major": "컴퓨터공학과, 인공지능학과",
            "personality": "논리적이고 혼자 집중 잘하는 사람",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "career": "📊 데이터 분석가",
            "major": "통계학과, 데이터사이언스학과",
            "personality": "분석 좋아하고 계획적인 사람",
            "salary": "평균 연봉 약 4,800만원"
        }
    ],

    "INTP": [
        {
            "career": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "호기심 많고 아이디어 넘치는 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "🔬 연구원",
            "major": "화학과, 물리학과",
            "personality": "탐구심 강하고 조용히 파고드는 스타일",
            "salary": "평균 연봉 약 4,700만원"
        }
    ],

    "ENTJ": [
        {
            "career": "🏢 CEO",
            "major": "경영학과, 경제학과",
            "personality": "리더십 있고 추진력 강한 사람",
            "salary": "평균 연봉 약 7,000만원 이상"
        },
        {
            "career": "📈 마케팅 기획자",
            "major": "광고홍보학과, 경영학과",
            "personality": "사람 이끄는 거 좋아하는 사람",
            "salary": "평균 연봉 약 4,600만원"
        }
    ],

    "ENTP": [
        {
            "career": "🎤 크리에이터",
            "major": "미디어학과, 방송연예과",
            "personality": "말 잘하고 아이디어 미친듯이 많은 사람",
            "salary": "평균 연봉 편차 큼 😵"
        },
        {
            "career": "🚀 스타트업 창업가",
            "major": "경영학과, 창업학과",
            "personality": "도전 좋아하고 지루한 거 싫어하는 사람",
            "salary": "성공하면 개높음 🔥"
        }
    ],

    "INFJ": [
        {
            "career": "🩺 상담심리사",
            "major": "심리학과, 상담학과",
            "personality": "공감 잘하고 사람 고민 잘 들어주는 사람",
            "salary": "평균 연봉 약 4,200만원"
        },
        {
            "career": "✍️ 작가",
            "major": "문예창작과, 국문과",
            "personality": "감수성 풍부하고 생각 깊은 사람",
            "salary": "수입 편차 큼"
        }
    ],

    "INFP": [
        {
            "career": "🎨 일러스트레이터",
            "major": "시각디자인과",
            "personality": "감성적이고 창의적인 사람",
            "salary": "평균 연봉 약 3,800만원"
        },
        {
            "career": "🎵 작곡가",
            "major": "실용음악과",
            "personality": "예술 감각 좋고 감정 표현 잘하는 사람",
            "salary": "성공 여부에 따라 차이 큼"
        }
    ],

    "ENFJ": [
        {
            "career": "👨‍🏫 교사",
            "major": "교육학과",
            "personality": "사람 챙기는 거 좋아하는 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "🤝 인사담당자",
            "major": "경영학과",
            "personality": "소통 잘하고 분위기 메이커인 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "ENFP": [
        {
            "career": "📹 유튜버",
            "major": "미디어학과",
            "personality": "텐션 높고 사람 좋아하는 사람",
            "salary": "편차 개큼 😂"
        },
        {
            "career": "🎉 이벤트 기획자",
            "major": "관광경영학과",
            "personality": "재밌는 거 좋아하고 활발한 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],

    "ISTJ": [
        {
            "career": "🏦 회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 강한 사람",
            "salary": "평균 연봉 약 6,000만원"
        },
        {
            "career": "⚖️ 공무원",
            "major": "행정학과",
            "personality": "안정적인 거 좋아하는 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "ISFJ": [
        {
            "career": "💉 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 성실한 사람",
            "salary": "평균 연봉 약 4,700만원"
        },
        {
            "career": "🏥 물리치료사",
            "major": "물리치료학과",
            "personality": "남 돕는 거 좋아하는 사람",
            "salary": "평균 연봉 약 4,300만원"
        }
    ],

    "ESTJ": [
        {
            "career": "👮 경찰",
            "major": "경찰행정학과",
            "personality": "책임감 강하고 리더십 있는 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "📋 관리자",
            "major": "경영학과",
            "personality": "체계적인 거 좋아하는 사람",
            "salary": "평균 연봉 약 5,200만원"
        }
    ],

    "ESFJ": [
        {
            "career": "✈️ 승무원",
            "major": "항공서비스학과",
            "personality": "친절하고 사교성 좋은 사람",
            "salary": "평균 연봉 약 4,800만원"
        },
        {
            "career": "🧑‍🍳 호텔리어",
            "major": "호텔관광학과",
            "personality": "서비스 정신 좋은 사람",
            "salary": "평균 연봉 약 4,200만원"
        }
    ],

    "ISTP": [
        {
            "career": "🔧 엔지니어",
            "major": "기계공학과",
            "personality": "손재주 좋고 문제 해결 좋아하는 사람",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "career": "🚗 자동차 정비사",
            "major": "자동차공학과",
            "personality": "직접 만지고 고치는 거 좋아하는 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],

    "ISFP": [
        {
            "career": "📸 사진작가",
            "major": "사진영상학과",
            "personality": "감각적이고 자유로운 사람",
            "salary": "평균 연봉 편차 큼"
        },
        {
            "career": "💄 메이크업 아티스트",
            "major": "뷰티학과",
            "personality": "꾸미는 거 좋아하는 사람",
            "salary": "평균 연봉 약 3,800만원"
        }
    ],

    "ESTP": [
        {
            "career": "💼 영업직",
            "major": "경영학과",
            "personality": "말빨 좋고 활동적인 사람",
            "salary": "인센 따라 높아짐 🔥"
        },
        {
            "career": "🏀 스포츠 트레이너",
            "major": "체육학과",
            "personality": "몸 움직이는 거 좋아하는 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],

    "ESFP": [
        {
            "career": "🎬 배우",
            "major": "연극영화과",
            "personality": "끼 많고 주목받는 거 좋아하는 사람",
            "salary": "편차 매우 큼 😎"
        },
        {
            "career": "🎧 DJ",
            "major": "실용음악과",
            "personality": "흥 많고 분위기 띄우는 사람",
            "salary": "경력 따라 달라짐"
        }
    ]
}

st.title("🔥 MBTI 진로 추천기")
st.write("애들아 너 MBTI 고르면 진로 2개 추천해준다 😎")

mbti_list = list(career_data.keys())

selected_mbti = st.selectbox(
    "✨ 너 MBTI 골라봐",
    mbti_list
)

if st.button("🚀 진로 추천 받기"):

    st.balloons()

    st.header(f"🔥 {selected_mbti} 추천 진로")

    careers = career_data[selected_mbti]

    for idx, item in enumerate(careers, start=1):
        st.subheader(f"{idx}. {item['career']}")

        st.write(f"📚 추천 학과 : {item['major']}")
        st.write(f"😎 잘 맞는 성격 : {item['personality']}")
        st.write(f"💰 평균 연봉 : {item['salary']}")

        st.markdown("---")

    random_msg = random.choice([
        "🔥 너 이쪽 재능 있을지도?",
        "😳 생각보다 잘 맞을 수도 있는데?",
        "🚀 미래 개쩔 수도 있음",
        "👀 은근 잘 어울리는 직업들임",
    ])

    st.success(random_msg)

st.caption("💡 재미로 보는 추천이라 너무 과몰입은 ㄴㄴ 😎")

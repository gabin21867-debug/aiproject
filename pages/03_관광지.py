# app.py
# Streamlit app showing Seoul top 10 attractions on a Folium map
# Save this file as app.py and the requirements listed below as requirements.txt

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top10 (for foreigners)", layout="wide")

st.title("서울 외국인이 좋아하는 관광지 Top 10 — 지도 표시 (Folium)")
st.markdown("간단한 설명: 왼쪽에서 장소를 선택하면 지도가 해당 위치로 이동하고 팝업 정보가 표시됩니다.")

# Top 10 attractions (name, lat, lon, short description)
ATTRACTIONS = [
    ("Gyeongbokgung Palace", 37.5796, 126.9770, "경복궁 — 조선 시대의 대표 궁궐"),
    ("Changdeokgung Palace & Huwon", 37.5794, 126.9910, "창덕궁과 후원 — 유네스코 세계문화유산"),
    ("Bukchon Hanok Village", 37.5826, 126.9830, "북촌 한옥마을 — 전통 한옥들이 모여 있는 마을"),
    ("N Seoul Tower (Namsan)", 37.5512, 126.9882, "남산서울타워 — 서울을 한눈에 보는 전망대"),
    ("Myeongdong Shopping Street", 37.5638, 126.9827, "명동 — 쇼핑과 길거리 음식의 중심지"),
    ("Insadong", 37.5740, 126.9849, "인사동 — 전통 찻집과 기념품 상점들"),
    ("Hongdae (Hongik Univ.)", 37.5563, 126.9226, "홍대 — 젊음의 문화와 거리공연"),
    ("Dongdaemun Design Plaza (DDP)", 37.5663, 127.0090, "동대문디자인플라자 — 현대적 건축 및 야시장"),
    ("Gwangjang Market", 37.5700, 127.0031, "광장시장 — 전통시장과 길거리 음식"),
    ("Lotte World Tower (Seoul Sky)", 37.5131, 127.1025, "롯데월드타워 — 전망대 및 쇼핑몰")
]

# Sidebar controls
st.sidebar.header("필터 & 설정")
show_list = st.sidebar.multiselect("지도에 표시할 관광지 선택 (모두 선택 가능)",
                                   [t[0] for t in ATTRACTIONS], default=[t[0] for t in ATTRACTIONS])

center_option = st.sidebar.selectbox("지도 중심 위치", ("Seoul Center", "First selected"))

# Build a dataframe for display
df = pd.DataFrame(ATTRACTIONS, columns=["Name", "Lat", "Lon", "Description"]) 
st.sidebar.dataframe(df)

# Initialize folium map
if center_option == "Seoul Center":
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
else:
    first = next((t for t in ATTRACTIONS if t[0] in show_list), ATTRACTIONS[0])
    m = folium.Map(location=[first[1], first[2]], zoom_start=14)

# Add markers
for name, lat, lon, desc in ATTRACTIONS:
    if name in show_list:
        popup_html = f"<b>{name}</b><br>{desc}<br><a href='https://www.google.com/search?q={name}+Seoul' target='_blank'>더 알아보기 (Google)</a>"
        folium.Marker([lat, lon], popup=popup_html, tooltip=name).add_to(m)

# Display map
st.header("지도 (Folium)")
st.markdown("팝업의 '더 알아보기' 링크는 구글 검색으로 연결됩니다.")
map_data = st_folium(m, width=1000, height=600)

# Show table of selected
st.header("선택된 관광지 목록")
st.table(df[df['Name'].isin(show_list)][['Name','Description']].reset_index(drop=True))

st.markdown("---")
st.caption("데이터 출처(예시): VisitSeoul, TripAdvisor, 및 서울시 관광 안내자료를 기반으로 정리함.")

# Footer with basic run instructions
st.markdown("**실행법 (로컬)**:\n1) 이 디렉토리에 app.py 파일을 저장하세요.\n2) requirements.txt에 필요한 패키지를 설치하세요: `pip install -r requirements.txt`\n3) `streamlit run app.py` 실행\n\n**Streamlit Cloud에 배포하려면**: 이 파일과 requirements.txt를 GitHub repo에 업로드한 뒤 Streamlit Cloud에서 해당 repo로 배포하세요.")

# End of app.py


# ------------------
# requirements.txt
# ------------------
# Save the following lines into a file named requirements.txt:
# streamlit
# folium
# streamlit-folium
# pandas

# ------------------
# README (간단)
# ------------------
# 파일: app.py (이 문서)
# 파일: requirements.txt (위 내용)
# 설명: Streamlit + Folium으로 서울 외국인 인기 관광지 Top10을 지도에 표시합니다.
# Tips: 더 많은 기능(이미지, 외부 API 링크, 사진 썸네일)을 추가하려면 알려주세요!
 

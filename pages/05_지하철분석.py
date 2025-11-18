# Streamlit page: 2025-10 하루별 호선별 역별 승하차 합계 시각화 (Plotly)
# 파일 위치: pages/10_october_2025_visualization.py (Streamlit pages 폴더에 넣어주세요)
# CSV 파일 경로(상위 폴더): ../subway.csv

import os
from datetime import date
import math
import io

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="2025-10 Subway — 역별 승하차 합계", layout="wide")

st.title("🟣 2025년 10월 — 호선별 역별 승하차 합계 (Interactive)")
st.markdown("CSV 파일 경로: `../subway.csv` — 이 파일이 앱을 실행하는 환경의 상위 폴더에 있어야 합니다.")

@st.cache_data
def load_data(path='../subway.csv'):
    # 한글 인코딩으로 읽기 (서울시 파일은 cp949/utf-8 중 하나일 가능성이 높음)
    try:
        df = pd.read_csv(path, encoding='cp949')
    except Exception:
        df = pd.read_csv(path, encoding='utf-8')

    # 사용일자 -> datetime
    if '사용일자' in

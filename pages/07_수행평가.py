
# pages/sport_cert_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="스포츠 자격증 시각화", layout="wide")
st.title("🏅 스포츠 종목별 자격증 현황 (Plotly)")

CSV_FILENAME = "sport.csv"
CSV_PATH = os.path.join(os.getcwd(), CSV_FILENAME)

# 1) CSV 존재 확인
if not os.path.exists(CSV_PATH):
    st.error(f"루트 폴더에 '{CSV_FILENAME}' 파일이 없습니다.\n프로젝트 루트에 업로드해 주세요.")
    st.info("CSV 예시 컬럼: 종목,급수,자격증수")
    st.stop()

# 2) CSV 읽기 (인코딩을 utf-8-sig 우선 시도)
df = None
for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
    try:
        df = pd.read_csv(CSV_PATH, encoding=enc)
        break
    except Exception:
        df = None
if df is None:
    st.error("CSV 파일을 읽는 데 실패했습니다. (인코딩 문제 가능성 있음)")
    st.stop()

st.subheader("원본 데이터 미리보기")
st.dataframe(df.head(10))

# 3) 필수 컬럼 검사 및 자동 매핑 시도
cols = list(df.columns)
cols_lower_to_orig = {c.lower(): c for c in cols}

# 기본 기대 컬럼명(한글)
expected_keys = {"종목": None, "급수": None, "자격증수": None}

# 자동 매핑 시도 (대소문자/소문자 기반)
for key in expected_keys.keys():
    if key in cols:
        expected_keys[key] = key
    elif key.lower() in cols_lower_to_orig:
        expected_keys[key] = cols_lower_to_orig[key.lower()]

st.markdown("---")
st.subheader("컬럼 매핑 (CSV에 컬럼명이 다르면 선택하세요)")
c1, c2, c3 = st.columns(3)
with c1:
    expected_keys["종목"]_

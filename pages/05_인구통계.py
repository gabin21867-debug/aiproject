# app.py
import re
import io
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- 페이지 설정
st.set_page_config(page_title="연령별 인구 꺾은선그래프", layout="wide")

st.title("연령별 인구 꺾은선그래프 (행정구 선택)")
st.caption("업로드된 엑셀 파일 또는 로컬 파일에서 행정구별 연령 인구를 꺾은선으로 표시합니다.")

# --- 파일 입력: 로컬 파일 경로가 있으면 우선 사용, 없으면 업로더 사용
LOCAL_DEFAULT = "/mnt/data/202510_202510_연령별인구현황_월간.xlsx"
uploaded_file = st.file_uploader("엑셀 파일 업로드 (없으면 앱 내 기본 파일 사용)", type=["xlsx", "xls"])

if uploaded_file is None and Path(LOCAL_DEFAULT).exists():
    # 로컬 파일 있으면 사용
    df_raw = pd.read_excel(LOCAL_DEFAULT, sheet_name=0)
    st.info(f"로컬 기본 파일을 사용합니다: {LOCAL_DEFAULT}")
else:
    if uploaded_file is None:
        st.warning("파일을 업로드하거나 레포지토리에 엑셀 파일을 넣어주세요.")
        st.stop()
    else:
        # 업로드된 파일 사용
        df_raw = pd.read_excel(uploaded_file, sheet_name=0)
        st.success("업로드된 파일을 불러왔습니다.")

st.write("데이터 미리보기 (상위 10행)")
st.dataframe(df_raw.head(10))

# --- 데이터 전처리: 여러 포맷 대비 범용 처리
def detect_and_melt(df):
    """다음 두 포맷을 자동 감지:
       A) Long format: columns include '행정구'(또는 '지역'), '연령' (or 'age'), '인구' (or 'population')
       B) Wide format: 한 행정구마다 연령별(0,1,2... 또는 '0세','1세') 컬럼이 여러개인 형태
       반환: DataFrame with columns ['행정구', 'age', 'population'] where age is int
    """
    df = df.copy()
    cols = [c for c in df.columns.astype(str)]
    lower = [c.lower() for c in cols]

    # 컬럼명 매핑 후보
    region_col = None
    for candidate in ['행정구', '행정구역', '지역', '시군구', '구', '행정동', 'area', 'region']:
        for c in cols:
            if candidate in str(c).lower():
                region_col = c
                break
        if region_col:
            break

    # long format 감지
    age_col = None
    pop_col = None
    for candidate in ['연령', '나이', 'age']:
        for c in cols:
            if candidate == str(c).lower() or candidate in str(c).lower():
                age_col = c
                break
        if age_col:
            break
    for candidate in ['인구', 'population', 'pop', '인구수']:
        for c in cols:
            if candidate == str(c).lower() or candidate in str(c).lower():
                pop_col = c
                break
        if pop_col:
            break

    # Case A: 이미 long format (region + age + population)
    if region_col and age_col and pop_col:
        df_long = df[[region_col, age_col, pop_col]].rename(columns={
            region_col: 'region', age_col: 'age', pop_col: 'population'
        })
        # age에서 숫자 추출
        df_long['age'] = df_long['age'].astype(str).str.extract(r'(\d{1,3})').astype(float).astype('Int64')
        df_long = df_long.dropna(subset=['age'])
        df_long['population'] = pd.to_numeric(df_long['population'], errors='coerce').fillna(0).astype(int)
        return df_long.rename(columns={'region':'행정구', 'age':'age', 'population':'population'})

    # Case B: wide format: 한 열이 region, 나머지가 나이 컬럼들
    # region_col가 발견되지 않으면 첫 컬럼을 region으로 사용
    region_col = region_col or cols[0]
    # age-like 컬럼 찾기: 컬럼명에 숫자가 포함된 것
    age_cols = []
    for c in co

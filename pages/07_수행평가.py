streamlit
pandas
plotly
openpyxl


# pages/자격증_시각화.py
# Streamlit page that reads a CSV from the repository root (or /mnt/data when running here)
# Shows interactive Plotly bar chart of certificate-grade counts per '종목'.

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="종목별 자격증 시각화", layout="wide")

st.title("종목별 자격증 등급 분포 — Plotly 인터랙티브")

# Robust path detection: prefer repo root 'sport.csv' but fall back to /mnt/data path if present
possible_paths = ["./sport.csv", "/mnt/data/sport.csv", "sport.csv"]
csv_path = None
for p in possible_paths:
    if os.path.exists(p):
        csv_path = p
        break

if csv_path is None:
    st.error("CSV 파일을 찾을 수 없습니다. 루트 폴더에 'sport.csv' 파일을 업로드했는지 확인하세요.")
    st.stop()

@st.cache_data
def load_data(path):
    # Try common encodings (utf-8, utf-8-sig, cp949/euc-kr, latin1)
    encs = [None, 'utf-8-sig', 'cp949', 'euc-kr', 'latin1']
    for e in encs:
        try:
            if e is None:
                df = pd.read_csv(path)
            else:
                df = pd.read_csv(path, encoding=e)
            return df
        except Exception:
            continue
    raise ValueError("CSV를 읽을 수 없습니다 (인코딩 문제). 파일 인코딩을 확인하세요.")

try:
    df = load_data(csv_path)
except Exception as e:
    st.exception(e)
    st.stop()

# Expecting at least columns: '종목' and many certificate columns like '1급 ..._2024년'
if '종목' not in df.columns:
    st.error("CSV에 '종목' 열이 없습니다. 파일의 컬럼을 확인해주세요.")
    st.write(df.columns.tolist())
    st.stop()

# Build a mapping of certificate base name -> list of columns (to aggregate across year columns)
# We assume the year suffix is like '_2024년', '_2023년', '_2022년 이전' etc.
cert_cols = [c for c in df.columns if c != '순번' and c != '종목']

# Normalize column base name by removing year suffixes
import re

def base_cert_name(col):
    # remove trailing underscore + year text
    return re.sub(r'_(?:\d{4}년|\d{4}년 이전)$', '', col).strip()

base_map = {}
for c in cert_cols:
    base = base_cert_name(c)
    base_map.setdefault(base, []).append(c)

# For UI: list of unique 종목 values
sports = df['종목'].dropna().unique().tolist()
if not sports:
    st.error("데이터에 사용할 수 있는 '종목' 값이 없습니다.")
    st.stop()

with st.sidebar:
    st.header("필터")
    sel_sport = st.selectbox("종목 선택", options=sorted(sports))
    top_n = st.slider("상위 몇 개 자격증을 표시할까요?", min_value=3, max_value=50, value=20)
    aggregate_years = st.checkbox("연도 합산 (모든 연도 합치기)", value=True)
    show_values = st.checkbox("그래프에 수치 표시", value=True)

# Filter dataframe to selected sport
sub = df[df['종목'] == sel_sport]
if sub.empty:
    st.warning("선택된 종목에 데이터가 없습니다.")
    st.stop()

# Aggregate counts for each base certificate (sum across year columns)
cert_sums = {}
for base, cols in base_map.items():
    try:
        # coerce to numeric and sum
        total = sub[cols].apply(pd.to_numeric, errors='coerce').sum(axis=1).fillna(0).sum()
        cert_sums[base] = int(total)
    except Exception:
        cert_sums[base] = 0

# Create DataFrame for plotting
plot_df = pd.DataFrame.from_dict(cert_sums, orient='index', columns=['count']).reset_index().rename(columns={'index':'certificate'})
plot_df = plot_df[plot_df['count']>0]
if plot_df.empty:
    st.info("해당 종목에 등록된 자격증 데이터가 없습니다 (값이 0 또는 결측).")
    st.stop()

plot_df = plot_df.sort_values('count', ascending=False).head(top_n)

# Plotly bar chart with color mapped to count using Reds colorscale so higher counts -> red
fig = px.bar(plot_df, x='certificate', y='count', title=f"{sel_sport} — 자격증별 보유수",
             text='count', labels={'certificate':'자격증', 'count':'보유수'},
             color='count', color_continuous_scale='Reds')
fig.update_layout(xaxis_tickangle=-45, uniformtext_minsize=8, uniformtext_mode='hide')

if show_values:
    fig.update_traces(texttemplate='%{text}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.write("데이터 샘플 (상위 10행)")
st.dataframe(df.head(10))

st.caption(f"데이터 파일 경로: `{csv_path}`")

# Helpful tips
with st.expander("사용 팁"):
    st.write("- CSV에 `종목` 컬럼이 있어야 합니다.")
    st.write("- 각 자격증은 연도별로 `_2024년`, `_2023년`, `_2022년 이전` 식으로 분리되어 있을 수 있습니다. 앱은 같은 자격증 이름을 합산하여 보여줍니다.")
    st.write("- 루트에 'sport.csv'를 올리고 Streamlit Cloud에 배포하면 pages 폴더의 이 파일이 자동으로 페이지로 보입니다.")


# ---------------------------
# requirements.txt (아래 내용을 루트의 requirements.txt 파일로 저장하세요)
# ---------------------------
# streamlit
# pandas
# plotly
# openpyxl  # if you need to read Excel files in future
# ---------------------------

# EOF

# Streamlit page: 2025-10 Subway Visualization
# File: pages/10_october_2025.py

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date

st.set_page_config(page_title="2025년 10월 지하철 승하차", layout="wide")
st.title("🟣 2025년 10월 — 호선·날짜별 역 승하차 분석")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../subway.csv', encoding='cp949')
    except:
        df = pd.read_csv('../subway.csv', encoding='utf-8')

    df['사용일자'] = df['사용일자'].astype(str)
    df['date'] = pd.to_datetime(df['사용일자'], format='%Y%m%d', errors='coerce')

    df['승차총승객수'] = df['승차총승객수'].fillna(0).astype(int)
    df['하차총승객수'] = df['하차총승객수'].fillna(0).astype(int)
    df['총승객수'] = df['승차총승객수'] + df['하차총승객수']

    return df

# Load
try:
    df = load_data()
except Exception as e:
    st.error(f"CSV 파일 로딩 실패: {e}")
    st.stop()

# Filter date range
oct_dates = df[df['date'].dt.month == 10]['date'].dt.date.unique()
if len(oct_dates) == 0:
    st.error("데이터에 10월 데이터가 없습니다.")
    st.stop()

default_date = sorted(oct_dates)[0]
selected_date = st.sidebar.date_input(
    "날짜 선택 (2025년 10월)",
    value=default_date,
    min_value=date(2025,10,1),
    max_value=date(2025,10,31)
)

lines = sorted(df['노선명'].dropna().unique())
selected_line = st.sidebar.selectbox("호선 선택", lines)

# Apply filters
filtered = df[(df['date'].dt.date == selected_date) & (df['노선명'] == selected_line)]

if filtered.empty:
    st.warning("선택한 조건에 해당하는 역 데이터가 없습니다.")
    st.stop()

# Aggregate
agg = (
    filtered.groupby('역명', as_index=False)
    .agg({'총승객수':'sum','승차총승객수':'sum','하차총승객수':'sum'})
    .sort_values('총승객수', ascending=False)
)

# Colors
def make_colors(n):
    first = (123, 10, 142)
    ochre_start = (198, 134, 43)
    ochre_end = (240, 224, 192)
    colors = []
    for i in range(n):
        if i == 0:
            colors.append(f"rgb({first[0]},{first[1]},{first[2]})")
        else:
            t = (i-1)/max(1,n-2)
            r = int(ochre_start[0] + (ochre_end[0]-ochre_start[0])*t)
            g = int(ochre_start[1] + (ochre_end[1]-ochre_start[1])*t)
            b = int(ochre_start[2] + (ochre_end[2]-ochre_start[2])*t)
            colors.append(f"rgb({r},{g},{b})")
    return colors

colors = make_colors(len(agg))

fig = px.bar(
    agg,
    x="역명",
    y="총승객수",
    hover_data=["승차총승객수", "하차총승객수"],
    title=f"{selected_date} — {selected_line} 승하차 합계"
)

fig.update_traces(marker_color=colors)
fig.update_layout(xaxis_tickangle=-45, yaxis_tickformat=',')

st.plotly_chart(fig, use_container_width=True)

st.subheader("데이터 테이블")
st.dataframe(agg)

st.download_button(
    "CSV 다운로드",
    agg.to_csv(index=False).encode('utf-8-sig'),
    file_name="subway_filtered.csv"
)

# requirements.txt 안내
st.markdown("""
### 📌 requirements.txt
```
streamlit
pandas
plotly
numpy
```
""")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="세계 MBTI 대시보드", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

st.title("🌍 국가별 MBTI 성향 분석 대시보드")

# 국가 선택
country = st.selectbox("국가를 선택하세요:", df["Country"].sort_values())

# 선택된 국가 데이터 추출
row = df[df["Country"] == country].iloc[0]
mbti_cols = [c for c in df.columns if c != "Country"]
values = row[mbti_cols].values

# 1등 MBTI 색상 설정
max_index = values.argmax()
colors = ["rgba(0, 102, 255, 0.6)" for _ in values]  # 기본 파란 그라데이션
colors[max_index] = "rgba(255, 0, 0, 0.8)"  # 1등 빨간색

# Plotly 그래프 생성
fig = go.Figure(data=[
    go.Bar(
        x=mbti_cols,
        y=values,
        marker_color=colors,
        text=[f"{v*100:.2f}%" for v in values],
        textposition="outside"
    )
])

fig.update_layout(
    title=f"🇺🇳 {country}의 MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis=dict(tickformat=".0%"),
    template="plotly_white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

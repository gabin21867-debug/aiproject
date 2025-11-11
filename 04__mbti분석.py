import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="세계 MBTI 대시보드", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()
mbti_cols = [c for c in df.columns if c != "Country"]

st.title("🌍 국가별 MBTI 성향 분석 대시보드")

# -----------------------------
# 1) 국가 선택 → 해당 국가 MBTI 비율 그래프
# -----------------------------
country = st.selectbox("국가를 선택하세요:", df["Country"].sort_values())
row = df[df["Country"] == country].iloc[0]
values = row[mbti_cols].values

# 색상 (1등 빨강 / 나머지 파란 그라데이션)
max_index = values.argmax()
colors = ["rgba(0, 102, 255, 0.6)" for _ in values]  # 기본 파란 톤
colors[max_index] = "rgba(255, 0, 0, 0.8)"  # 1등 빨강

fig_country = go.Figure(data=[
    go.Bar(
        x=mbti_cols,
        y=values,
        marker_color=colors,
        text=[f"{v*100:.2f}%" for v in values],
        textposition="outside"
    )
])

fig_country.update_layout(
    title=f"🇺🇳 {country}의 MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis=dict(tickformat=".0%"),
    template="plotly_white",
    height=550
)

st.plotly_chart(fig_country, use_container_width=True)


# -----------------------------
# 2) MBTI 선택 → 해당 MBTI 비율 높은 국가 TOP 그래프
# -----------------------------
st.markdown("---")
st.subheader("📊 MBTI 유형 기준 국가 순위")

selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_cols)

# 해당 MBTI로 국가 정렬
rank_df = df[["Country", selected_mbti]].sort_values(selected_mbti, ascending=False)

# 색상 규칙: 1등 노란, 한국 파란, 나머지 회색
bar_colors = []
for idx, row in rank_df.iterrows():
    country_name = row["Country"]
    if idx == rank_df.index[0]:
        bar_colors.append("rgba(255, 215, 0, 0.9)")  # 1등 노란색 (Gold)
    elif country_name.lower() in ["korea", "south korea", "republic of korea", "korea, south"]:
        bar_colors.append("rgba(0, 102, 255, 0.9)")  # 한국 파란색
    else:
        bar_colors.append("rgba(160,160,160,0.7)")  # 기본 회색

fig_mbti = go.Figure(data=[
    go.Bar(
        x=rank_df["Country"],
        y=rank_df[selected_mbti],
        marker_color=bar_colors,
        text=[f"{v*100:.2f}%" for v in rank_df[selected_mbti]],
        textposition="outside"
    )
])

fig_mbti.update_layout(
    title=f"🌐 {selected_mbti} 유형이 높은 국가 순위",
    xaxis_title="국가",
    yaxis_title="비율",
    yaxis=dict(tickformat=".0%"),
    template="plotly_white",
    height=600
)

st.plotly_chart(fig_mbti, use_container_width=True)

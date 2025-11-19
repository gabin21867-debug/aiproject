import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 제목
st.title("🏅 스포츠 종목별 자격증 현황 시각화")

# CSV 불러오기 (루트 폴더)
df = pd.read_csv("sport.csv")

# 종목 리스트 생성
sports = df['종목'].unique()
selected_sport = st.selectbox("종목을 선택하세요", sports)

# 선택된 종목 필터링
data = df[df['종목'] == selected_sport]

# 자격증 수 기준 색상(빨강 → 연한색)
max_val = data['자격증수'].max()

# 색상 스케일: 빨강 계열 그라데이션
color_scale = [
    [0, "#ffcccc"],  # 연한 빨강
    [0.5, "#ff6666"],
    [1, "#cc0000"]   # 진한 빨강
]

# Plotly 막대 그래프
fig = px.bar(
    data,
    x="급수",
    y="자격증수",
    title=f"{selected_sport} 종목의 자격증 급수 분포",
    color="자격증수",
    color_continuous_scale=color_scale,
    text="자격증수"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="급수",
    yaxis_title="자격증 수",
    coloraxis_showscale=False,
)

st.plotly_chart(fig, use_container_width=True)
```

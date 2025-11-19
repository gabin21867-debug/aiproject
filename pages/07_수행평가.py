
    import streamlit as st
selected = st.selectbox("종목을 선택하세요", sports)
filtered = df2[df2['종목'] == selected]


if filtered.empty:
st.warning("선택한 종목의 데이터가 없습니다.")
st.stop()


# 그래프 그리기
# 색상 스케일: 연한 -> 진한 빨강. Plotly의 Reds 사용해도 무방.
color_scale = ["#fff5f5", "#ffcccc", "#ff9999", "#ff6666", "#ff3333", "#cc0000"]


fig = px.bar(
filtered,
x='급수',
y='자격증수',
text='자격증수',
title=f"{selected} - 자격증 급수 분포",
color='자격증수',
color_continuous_scale=color_scale,
labels={'자격증수':'자격증 수', '급수':'급수'}
)


fig.update_traces(textposition='outside')
fig.update_layout(
xaxis_title='급수',
yaxis_title='자격증 수',
uniformtext_minsize=8,
uniformtext_mode='hide',
coloraxis_showscale=False,
margin=dict(l=40, r=20, t=60, b=40)
)


# y축의 그리드 간격(예: 100 단위로 보기를 원하면 아래 dtick 변경 가능)
max_y = int(filtered['자격증수'].max())
if max_y > 0:
# 자동으로 적당한 dtick 설정: 만약 최대가 매우 크면 1000단위, 보통은 10/50/100
if max_y <= 50:
dtick = 5
elif max_y <= 200:
dtick = 10
elif max_y <= 2000:
dtick = 100
else:
dtick = round(max_y / 10, -1)
fig.update_yaxes(dtick=dtick)


st.plotly_chart(fig, use_container_width=True)


# 데이터 다운로드 링크 (필요하면 사용)
@st.cache_data
def to_csv(df):
return df.to_csv(index=False).encode('utf-8-sig')


csv = to_csv(filtered)
st.download_button("현재 필터 데이터 다운로드 (CSV)", data=csv, file_name=f"{selected}_certs.csv", mime='text/csv')

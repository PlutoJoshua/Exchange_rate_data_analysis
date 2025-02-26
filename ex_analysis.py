import pandas as pd
from data import load_data, sort_data
from visual import plot_time_series_px
import plotly.express as px
import streamlit as st

df = load_data()
usd = sort_data(df, 'USD')
# print(usd.describe())

jpy = sort_data(df, 'JPY')
# print(jpy.describe())

# 환율 변화 차이(전 값과 비교, 절대값)
usd.loc[:, 'diff'] = usd['basePrice'].diff().abs()
jpy.loc[:, 'diff'] = jpy['basePrice'].diff().abs()

st.header("Ex analysis Dashboard")
# 통화 선택 드롭다운 추가
currency = st.sidebar.selectbox("Select Currency", ['USD', 'JPY'])

tab1, tab2 = st.tabs(['basic', 'diff'])

with tab1:
    if currency == 'USD':
        st.plotly_chart(plot_time_series_px(usd, 'USD'))
        st.plotly_chart(px.line(usd, x='createdAt', y='diff', title='USD'))
    elif currency == 'JPY':
        st.plotly_chart(plot_time_series_px(jpy, 'JPY'))
        st.plotly_chart(px.line(jpy, x='createdAt', y='diff', title='JPY'))
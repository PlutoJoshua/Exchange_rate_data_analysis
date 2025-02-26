import pandas as pd
from data import load_data, sort_data
from visual import plot_time_series_px
import streamlit as st

df = load_data()
usd = sort_data(df, 'USD')
# print(usd.describe())

jpy = sort_data(df, 'JPY')
# print(jpy.describe())

st.header("Ex analysis Dashboard")

tab1, tab2 = st.tabs(['basic', 'diff'])

with tab1:
    st.plotly_chart(plot_time_series_px(usd, 'USD'))
    st.plotly_chart(plot_time_series_px(jpy, 'JPY'))


import pandas as pd
from data import load_data, sort_data, calculate_price_difference
from visual import plot_time_series_px, plot_weekly_subplots, time_slot, plot_price_difference, box_plot, time_slot_price_diff
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
hour = st.sidebar.number_input("input number", min_value=1, value=3)
tab1, tab2 = st.tabs(['basic', 'diff'])

with tab1:
    if currency == 'USD':
        st.plotly_chart(plot_time_series_px(usd, 'USD'))
        st.markdown("---")
        st.plotly_chart(px.line(usd, x='createdAt', y='diff', title='USD'))
        st.markdown("---")        
        st.plotly_chart(plot_weekly_subplots(usd))


    elif currency == 'JPY':
        st.plotly_chart(plot_time_series_px(jpy, 'JPY'))
        st.markdown("---")
        st.plotly_chart(px.line(jpy, x='createdAt', y='diff', title='JPY'))
        st.markdown("---")
        st.plotly_chart(plot_weekly_subplots(jpy))

with tab2:
    if currency == 'USD':
        st.plotly_chart(time_slot(usd))
        filter_df = calculate_price_difference(usd, hour)
        st.plotly_chart(time_slot_price_diff(filter_df))
        st.plotly_chart(px.box(usd, y='basePrice', title='Box Plot of basePrice'))

        
        st.plotly_chart(plot_price_difference(filter_df))
        df_resampled = usd.resample("1h", on='createdAt')['diff'].mean().dropna()
        st.plotly_chart(px.line(df_resampled, x=df_resampled.index, y=df_resampled.values))
        st.plotly_chart(box_plot(filter_df))
        st.markdown("---")
        sort = filter_df.sort_values(by='price_diff', ascending=False)
        st.dataframe(sort)
    elif currency == 'JPY':
        st.plotly_chart(time_slot(jpy))
        filter_df = calculate_price_difference(jpy, hour)
        st.plotly_chart(time_slot_price_diff(filter_df))
        st.plotly_chart(px.box(jpy, y='basePrice', title='Box Plot of basePrice'))

        st.plotly_chart(plot_price_difference(filter_df))      
        df_resampled = jpy.resample("1h", on='createdAt')['diff'].mean().dropna()
        st.plotly_chart(px.line(df_resampled, x=df_resampled.index, y=df_resampled.values))    
        st.plotly_chart(box_plot(filter_df))
        st.markdown("---")
        filter_df_0 = filter_df.copy()
        filter_df_0 = filter_df_0[filter_df_0['price_diff'] !=0.0]
        sort = filter_df_0.sort_values(by='price_diff', ascending=False)
        st.dataframe(sort.describe())
        # price_diff가 1.2 이상인 데이터 필터링
        high_price_diff_df = filter_df_0[filter_df_0['price_diff'] >= 1.2]
        st.plotly_chart(px.line(high_price_diff_df, x='createdAt', y='price_diff', title='Price Difference >= 1.2')) 
        st.dataframe(sort)

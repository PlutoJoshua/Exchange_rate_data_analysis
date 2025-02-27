import pandas as pd
from data import load_data, sort_data, calculate_price_difference
from visual import plot_time_series_px, plot_weekly_subplots, time_slot, plot_price_difference, box_plot, time_slot_price_diff, plot_price_distribution_histogram
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
        st.plotly_chart(px.box(usd, y='basePrice', title='Box Plot of basePrice'))
        st.plotly_chart(px.line(usd, x='createdAt', y='diff', title='USD'))
        st.markdown("---")        
        st.plotly_chart(plot_weekly_subplots(usd))

    elif currency == 'JPY':
        st.plotly_chart(plot_time_series_px(jpy, 'JPY'))
        st.markdown("---")
        st.plotly_chart(px.box(jpy, y='basePrice', title='Box Plot of basePrice'))
        st.plotly_chart(px.line(jpy, x='createdAt', y='diff', title='JPY'))
        st.markdown("---")
        st.plotly_chart(plot_weekly_subplots(jpy))

with tab2:
    if currency == 'USD':
        st.plotly_chart(time_slot(usd))

        # 원하는 시간대로 데이터 필터링
        filter_df = calculate_price_difference(usd, hour)
        st.plotly_chart(time_slot_price_diff(filter_df))
        st.plotly_chart(plot_price_difference(filter_df))
        df_resampled = usd.resample("1h", on='createdAt')['diff'].mean().dropna()
        st.plotly_chart(px.line(df_resampled, x=df_resampled.index, y=df_resampled.values))
        count_zero_diff = (filter_df['price_diff'] == 0.0).sum()  # price_diff가 0.0인 갯수
        total_count = len(filter_df)  # 전체 갯수
        st.markdown(f'Price difference == 0.0: {count_zero_diff} out of {total_count} / {(count_zero_diff / total_count).round(2) * 100} %')
        st.plotly_chart(box_plot(filter_df))
        sort = filter_df.sort_values(by='price_diff', ascending=False)
        st.markdown("---")
        st.plotly_chart(plot_price_distribution_histogram(filter_df))
        st.dataframe(sort)
    elif currency == 'JPY':
        st.plotly_chart(time_slot(jpy))
        
        # 원하는 시간대로 데이터 필터링
        filter_df = calculate_price_difference(jpy, hour)
        st.plotly_chart(time_slot_price_diff(filter_df))
        st.plotly_chart(plot_price_difference(filter_df))
        df_resampled = usd.resample("1h", on='createdAt')['diff'].mean().dropna()
        st.plotly_chart(px.line(df_resampled, x=df_resampled.index, y=df_resampled.values))
        count_zero_diff = (filter_df['price_diff'] == 0.0).sum()  # price_diff가 0.0인 갯수
        total_count = len(filter_df)  # 전체 갯수
        st.markdown(f'Price difference == 0.0: {count_zero_diff} out of {total_count} / {(count_zero_diff / total_count).round(2) * 100} %')
        st.plotly_chart(box_plot(filter_df))
        sort = filter_df.sort_values(by='price_diff', ascending=False)
        st.markdown("---")
        st.plotly_chart(plot_price_distribution_histogram(filter_df))
        st.dataframe(sort)

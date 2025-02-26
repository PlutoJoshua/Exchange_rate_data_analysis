import plotly.express as px

# function
def plot_time_series_px(df, currency_code):
    fig = px.line(df, x='createdAt', y='basePrice', title=f'{currency_code} Time series')  # Plotly를 사용한 시각화
    fig.update_layout(xaxis_title='Date', yaxis_title='Base Price')
    return fig


import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

# function
def plot_time_series_px(df, currency_code):
    fig = px.line(df, x='createdAt', y='basePrice', title=f'{currency_code} Time series')  # Plotly를 사용한 시각화
    fig.update_layout(xaxis_title='Date', yaxis_title='Base Price')

    # 변동성 계산
    vol = df['basePrice'].std()
    mean = df['basePrice'].mean()
    # 변동성 범위 추가 (배열로 변환)
    upper_volatility = [mean + vol] * len(df)
    lower_volatility = [mean - vol] * len(df)

    # 변동성 범위 추가
    fig.add_scatter(x=df['createdAt'], y=upper_volatility, mode='lines', name='Upper Volatility', line=dict(dash='dash', color='red'))
    fig.add_scatter(x=df['createdAt'], y=lower_volatility, mode='lines', name='Lower Volatility', line=dict(dash='dash', color='blue'))
    return fig

def plot_weekly_subplots(df):
    df['week'] = df['createdAt'].dt.to_period('W').astype(str)
    weeks = df['week'].unique()
    num_weeks = len(weeks)

    num_cols = 1
    num_rows = (num_weeks + num_cols - 1) // num_cols
    fig = sp.make_subplots(rows=num_rows, cols=num_cols, subplot_titles=weeks)

    for i, week in enumerate(weeks):
        week_data = df[df['week'] == week]
        fig.add_trace(
            go.Scatter(x=week_data['createdAt'], y=week_data['diff'], mode='lines', name=week),
            row=(i // num_cols) + 1,
            col=(i % num_cols) + 1
        )

    fig.update_layout(title_text='weekly', height=600 * num_rows, showlegend=False)
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='diff')
    return fig


def time_slot(df):
    time_slot_diff = df.groupby(df['createdAt'].dt.hour)['diff'].mean().reset_index()
    fig = px.line(time_slot_diff, x='createdAt', y='diff', title='diff for hour')
    return fig

def time_slot_price_diff(df):
    time_slot_diff = df.groupby(df['createdAt'].dt.hour)['price_diff'].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_slot_diff['createdAt'], 
                             y=time_slot_diff['price_diff'], 
                             mode='lines+markers+text', 
                             name='Price Difference',
                             text=[f'{value:.1f}' for value in time_slot_diff['price_diff']],  # 소수점 첫째 자리 표시
                             textposition='top center'))  # 텍스트 위치
    fig.update_layout(title='price_diff for hour')
    return fig
# 시각화
def plot_price_difference(df):
    fig = go.Figure()
    
    # 기본 라인 그래프
    fig.add_trace(go.Scatter(x=df['createdAt'], y=df['price_diff'], mode='lines', name='Price Difference'))
    
    # 상위 값 표시
    top = df.nlargest(30, 'price_diff')
    fig.add_trace(go.Scatter(
        x=top['createdAt'],
        y=top['price_diff'],
        mode='markers+text',
        name='Top Values',
        text=[f'{value:.1f}' for value in top['price_diff']],
        textposition='top center',
        marker=dict(size=5, color='red')
    ))
    
    fig.update_layout(title='Price Difference',
                      xaxis_title='Date',
                      yaxis_title='Price Difference',
                      showlegend=True)
    return fig

def box_plot(df):
    df = df.dropna()
    df = df[df['price_diff'] !=0.0]
    fig = px.box(df, y='price_diff', title='Box Plot of Price Differences')
    fig.update_layout(yaxis_title='Price Difference')
    return fig

def plot_price_distribution_histogram(df):
    # 상위 50개 값 선택
    top = df.nlargest(100, 'price_diff')
    
    # 시간대별로 분포를 나타내는 히스토그램
    fig = px.histogram(top, x=top['createdAt'].dt.hour, title='Price Difference Distribution by Hour')
    fig.update_layout(xaxis_title='Hour of Day', yaxis_title='Count')
    # Add text annotations for each bar
    fig.update_traces(texttemplate='%{y}', textposition='outside')  # Display count on top of bars
    fig.update_layout(xaxis_title='Hour of Day', yaxis_title='Count')
    return fig
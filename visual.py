import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

# function
def plot_time_series_px(df, currency_code):
    fig = px.line(df, x='createdAt', y='basePrice', title=f'{currency_code} Time series')  # Plotly를 사용한 시각화
    fig.update_layout(xaxis_title='Date', yaxis_title='Base Price')
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

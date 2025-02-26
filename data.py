import pandas as pd
import json
import matplotlib.pyplot as plt
import streamlit as st

# 데이터 로드 함수
@st.cache_data
def load_data():
    # 매매기준율 데이터 로드 및 전처리 코드
    df = pd.read_csv('../sql_data/mama.csv', sep='\t', dtype=str)
    df.columns = ['createdAt,data']
    df = df['createdAt,data'].str.split(',', n=1, expand=True)
    df.columns = ['createdAt', 'data']
    
    # JSON 파싱 함수
    def parse_json(json_str, created_at=None):
        try:
            # 앞부분 따옴표 제거
            json_str = json_str.replace('"{"result":', '{"result":')
            # 뒷부분 따옴표 제거
            if json_str.endswith('}]}"'): # '}]}"'로 끝나는지 확인
                json_str = json_str[:-1]
            data = json.loads(json_str)
            result_df = pd.DataFrame(data['result'])
            # 시간 추가
            if created_at is not None:
                result_df['createdAt'] = created_at
            return result_df
        except Exception as e:
            return None

    # 전체 데이터 처리
    parsed_data = []
    for _, row in df.iterrows(): # 각 행 순회
        result = parse_json(row['data'], row['createdAt'])
        if result is not None:
            result['createdAt'] = pd.to_datetime(result['createdAt'], format='%Y-%m-%d %H:%M:%S') + pd.Timedelta(hours=9) # UTC -> KST
            parsed_data.append(result)
    
    final_df = pd.concat(parsed_data, ignore_index=True)
    
    return final_df

@st.cache_data
def sort_data(df, code):
    df = df[df['currencyCode'] == f'{code}']
    df = df[['currencyCode', 'basePrice', 'createdAt']]
    return df

# 시간 별 비교를 위한 데이터 세팅
def calculate_price_difference(df, hour):
    # createdAt을 기준으로 정렬
    df = df.sort_values(by='createdAt')
    
    # 가격 차이를 저장할 리스트
    price_diffs = []

    # 이후 시간 계산을 저장할 리스트
    future_times = []
    
    for index, row in df.iterrows():
        target_time = row['createdAt'] + pd.Timedelta(hours=hour)
        # target_time 이후의 데이터 중 가장 가까운 가격 찾기
        future_prices = df[df['createdAt'] > target_time]
        
        if not future_prices.empty:
            closest_price = future_prices.iloc[0]['basePrice']
            price_diff = abs(closest_price - row['basePrice'])
        else:
            price_diff = None  # 이후 가격이 없을 경우
        
        price_diffs.append(price_diff)
        future_times.append(target_time)  # 이후 시간 추가
    
    df['price_diff'] = price_diffs
    df['future_time'] = future_times  # df에 이후 시간 추가
    return df
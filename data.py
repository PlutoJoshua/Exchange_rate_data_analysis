import pandas as pd
import json
import matplotlib.pyplot as plt

# 데이터 로드 함수
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

def sort_data(df, code):
    df = df[df['currencyCode'] == f'{code}']
    df = df[['currencyCode', 'basePrice', 'createdAt']]
    return df
import pandas as pd
from data import load_data, sort_data

df = load_data()
usd = sort_data(df, 'USD')
print(usd.describe())

jpy = sort_data(df, 'JPY')
print(jpy.describe())
import pandas as pd
from data import load_data

df = load_data()
usd = df[df['currencyCode'] == 'USD']
usd = usd[['currencyCode', 'basePrice', 'createdAt']]
print(usd)
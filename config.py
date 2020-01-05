import os

token = os.getenv('TOKEN')
data_mall_key = os.getenv('DATA_MALL_KEY')
print(token, data_mall_key)
query_base = f'https://api.telegram.org/bot{token}'
print(query_base)
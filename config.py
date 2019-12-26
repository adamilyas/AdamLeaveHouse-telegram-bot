token = "CHANGE THIS TOKEN ACCORDINGLY"
query_base = f'https://api.telegram.org/bot{token}'
# print(query_base)
chat_id = 'GET YOUR OWN CHAT ID YO'
print(f'{query_base}/sendMessage?chat_id={chat_id}&text=Hello')
import os

"""
export TOKEN='<TOKEN>';
export DATA_MALL_KEY='<KEY>';
echo $TOKEN;
echo $DATA_MALL_KEY;
"""
token = os.getenv('TOKEN')
data_mall_key = os.getenv('DATA_MALL_KEY')
query_base = f'https://api.telegram.org/bot{token}'

# constants
BOT_NAME = "@LeaveHouseBot"
TEXT = 'text'
HELP = '/help'
DELETE = '/del'
ADD = '/add'
DETAILS = '/details'
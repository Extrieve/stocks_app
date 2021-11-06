from stocks import data
from models import db, Stocks
import requests

# Pass all the api info to the db
# TODO: make a generator to pass the fast api calls

token = 'Tsk_1c42cee11b834d83b84aec96ae542f1a'


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


symbol_groups = list(chunks(data, 100))

symbol_strings = []

add_db = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

for symbol_string in symbol_strings:
    batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={token}'
    data = requests.get(batch_api_url).json()
    for symbol in symbol_string.split(','):
        ticker = symbol
        name = data[symbol]['quote']['companyName']
        latest_price = data[symbol]['quote']['latestPrice']
        average_volume = data[symbol]['quote']['avgTotalVolume']
        fifty_high = data[symbol]['quote']['week52High']
        fifty_low = data[symbol]['quote']['week52Low']
        iex_volume = data[symbol]['quote']['iexVolume']
        exchange = data[symbol]['quote']['primaryExchange']

        new_stock = Stocks(symbol=ticker, name=name, latest_price=latest_price, average_volume=average_volume,
                           fifty_high=fifty_high, fifty_low=fifty_low, iex_volume=iex_volume, primary_exchange=exchange)
        add_db.append(new_stock)

for item in add_db:
    try:
        db.session.add(item)
        db.session.commit()
    except:
        pass

# Stocks.query.delete()
# db.session.commit()

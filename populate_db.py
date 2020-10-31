import sqlite3
import alpaca_trade_api as tradeapi
import config
import os

connection = sqlite3.connect(os.path.join(os.getcwd(), 'app.db'))
connection.row_factory = sqlite3.Row
BASE_URL = "https://paper-api.alpaca.markets"

cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, company FROM stock
""")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]  # list comprehension

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=BASE_URL)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()
print(connection.total_changes, 'changes were made')

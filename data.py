from websockets import connect
import asyncio
import sys
import aiosqlite
import sqlite3
import json

### create cursor connection to obtain data

conn = sqlite3.connect("./data.db")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS trades")
cursor.execute(""" CREATE TABLE trades(
                id int PRIMARY KEY,
                time int,
                quantity int,
               price float) """)

cursor.execute("CREATE INDEX index_time ON trades(time)")

conn.commit()

conn.close()

url = "wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

async def save_down(url):

    
    async with connect(url) as websocket:

        trades_buffer =[] ### create an empty list to append each trade

        while True:
            data = await websocket.recv()
            data = json.loads(data) ### binance sends data as str object - hence convert to dictionary
            trades_buffer.append((data['a'], data['T'], data['q'], data['p'])) ### pass in as tuple

            print(data)

            if len(trades_buffer) > 10:
                
                print("Writing to DB")

                async with aiosqlite.connect("./data.db") as db:

                    await db.executemany("""INSERT INTO trades(id, time, quantity, price)
                                         VALUES(?,?,?,?)""", trades_buffer)
                    await db.commit()

                trades_buffer = []
            

asyncio.run(save_down(url))
               
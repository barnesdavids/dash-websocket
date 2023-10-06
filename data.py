import asyncio
import sys
import aiosqlite
import sqlite3
import json

conn = sqlite3.connect('./data.db')

cursor = conn.cursor()

cursor.execute(" DROP TABLE IF EXISTS trades ")
cursor.execute(""" CREATE TABLE trades(
                id int PRIMARY KEY,
                time int,
                quantity int,
               price float)""")

cursor.execute("CREATE INDEX index_time ON trades(time)")

conn.commit()

conn.close()
               
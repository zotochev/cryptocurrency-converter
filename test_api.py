import requests
import json
import sqlite3


conn = sqlite3.connect('tokens.db')
cursor = conn.cursor()

cursor.execute('''
          CREATE TABLE IF NOT EXISTS tokens 
          ([id] TEXT PRIMARY KEY, [symbol] TEXT, [name] TEXT)
          ''')
          
conn.commit()


r = requests.get('https://api.pancakeswap.info/api/v2/tokens')

for token in r.json()['data'].items():
    cursor.execute("insert into tokens values (?, ?, ?) ", [token[0], token[1]['symbol'].lower(), token[1]['name'].lower()])

conn.commit()
print(cursor.execute("SELECT * FROM tokens").fetchall())
conn.close()

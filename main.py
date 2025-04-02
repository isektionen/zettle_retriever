import requests
from dotenv import load_dotenv
import os
import psycopg2
import requests
from datetime import datetime

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
API_KEY = os.environ.get("CLIENT_SECRET")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")


connection = psycopg2.connect(
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    dbname=DBNAME
)

cursor = connection.cursor()
# Create the table if it doesn't exist
'''
cursor.execute("SELECT * FROM beers ORDER BY date DESC LIMIT 1")
result = cursor.fetchone()
last_update = result[0]
last_count = result[1]
cursor.close()
'''

last_update = "2025-03-01"
new_beer_count = 0

url = "https://oauth.zettle.com/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "client_id": f"{CLIENT_ID}",
    "assertion": f"{API_KEY}"
}

response = requests.post(url, headers=headers, data=data)
access_token = response.json()["access_token"]

url = "https://purchase.izettle.com/purchases/v2"
headers = {
    "Authorization": f"Bearer {access_token}"
}
params = {
    "startDate": last_update,
}

response = requests.get(url, headers=headers, params=params)

data = response.json() 

for purchase in data.get("purchases", []):
    for product in purchase.get("products", []):
        print()
        print(product.get('name', 'Unnamed Product'))
        if "öl" in product.get('name', 'Unnamed Product').lower():
            print("counting beer")
            new_beer_count += int(product.get('quantity', 0))

print(f"New beer count: {new_beer_count}")
'''
cursor = connection.cursor()
cursor.execute("INSERT INTO beers (date, count) VALUES (%s, %s)", (datetime.now().date(), new_beer_count+last_count))
connection.commit()
connection.close()
'''
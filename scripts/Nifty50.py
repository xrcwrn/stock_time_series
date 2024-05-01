#NSE ticker
import json
import requests
import threading
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import urllib.request, json 
from bs4 import BeautifulSoup
location="London"

DELAY = 5.0  # Time between calls in seconds.

ticker="NIFTY_50"
exchange="INDEXNSE"
def call_API(event):
  url=f'https://www.google.com/finance/quote/{ticker}:{exchange}'
  print(url)
  response=requests.get(url)
  soup=BeautifulSoup(response.text,"html.parser")
  class1="YM1Kec fxKbKc"
  name=soup.find(class_="zzDege").text
  price=float(soup.find(class_="YMlKec fxKbKc").text.strip().replace(",",""))
  print(name," " ,price)

  #Inserting to time series database
  bucket = "stockmarket"
  org = "IITBhilai"
  token = "0pX-BryNp3b6zz5qhWFxCjw6Iuln6YNwz7KTA9ygv5JIoyE39evjK5kPELyv-HQnREla3xubcAL0iNAIM8JdrA=="
  # Store the URL of your InfluxDB instance
  url="http://localhost:8086/"
  client = influxdb_client.InfluxDBClient(
     url=url,
     token=token,
     org=org
   )
  #writing to table
  write_api = client.write_api(write_options=SYNCHRONOUS)
  p = influxdb_client.Point("nifty50_live").tag("name", name).field("price", price)
  write_api.write(bucket=bucket, org=org, record=p)

  event.set()  # Signal call has been made.

print('Running')
event = threading.Event()
while True:
    event.clear()
    timer = threading.Timer(DELAY, call_API, (event,))  # Call after delay.
    timer.start()
    event.wait()  # Blocks until event is set by another thread.

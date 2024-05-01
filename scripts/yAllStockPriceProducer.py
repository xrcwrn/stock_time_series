import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import threading
from confluent_kafka import Producer, Consumer
import time



DELAY = 1.0  # Time between calls in seconds.
current_timestamp =0

def get_stats(ticker):
    info = yf.Tickers(ticker).tickers[ticker].info
    print(f"{ticker} {info['currentPrice']}")
    
    message={'price':info['currentPrice'],'timestamp':current_timestamp}
    p = Producer({'bootstrap.servers': 'localhost:9092'})
    p.produce(ticker, message)
    p.flush()  


def call_API(event):
    ticker_list = ['DLF.NS','SBIN.NS','HDFCBANK.NS','RELIANCE.NS','ICICIBANK.NS','INFY.NS','LT.NS','TCS.NS','ITC.NS','AXISBANK.BO','BHARTIARTL.NS']
    #ticker_list = ['DLF.NS']
    current_timestamp = time.time()
    
    with ThreadPoolExecutor() as executor:
        executor.map(get_stats, ticker_list)

    event.set()  # Signal call has been made.

print('Running')
event = threading.Event()
while True:
    event.clear()
    timer = threading.Timer(DELAY, call_API, (event,))  # Call after delay.
    timer.start()
    event.wait()  # Blocks until event is set by another thread.

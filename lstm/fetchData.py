import yfinance as yf
import pandas as pd
import streamlit as st
import time
import schedule
from lstm import Lstm
from datetime import date


ticker_symbol="DLF.NS"
startDate="2023-01-10"
endDate=date.today()
      

def predict():
    stock_data = fetch_stock_data()
    lstm = Lstm(stock_data)
    model = lstm.train_model()
    X_test, y_test, scaler = lstm.test_model()
    predicted_stock_price_with_actual, days = lstm.predict_price(X_test,y_test,model,scaler, endDate)
    create_plot(stock_data, predicted_stock_price_with_actual, days)
    print("Plot created successfully")
    
    
   
    
def fetch_stock_data():
    try:
      data = yf.download(ticker_symbol, start=startDate, end=endDate)
      print('Data Downloaded')
      return data
    except Exception as e:
      print("Unable to load data", str(e))
      return None

def create_plot(stock_data, predicted_stock_price_with_actual, days):
        import matplotlib.pyplot as plt
        from matplotlib.dates import DateFormatter, DayLocator

        # Plot the historical stock prices
        fig = plt.figure(figsize=(16, 10))
        plt.plot(stock_data.index, stock_data['Close'], label='Actual')
        plt.title(f"{ticker_symbol} Stock Price")
        plt.xlabel("Data")
        plt.ylabel("Cena")

        # Set the x-axis tick locator and formatter
        plt.gca().xaxis.set_major_locator(DayLocator(interval=7))
        plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))

        #  Plot the predicted stock prices with the last actual price at the beginning
        predicted_dates = pd.bdate_range(start=endDate, periods=len(predicted_stock_price_with_actual))
        plt.plot(predicted_dates[:days+1], predicted_stock_price_with_actual[:days+1], label='Predicted')

        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()

        st.subheader("Closing Price vs Date chart")
        st.pyplot(fig)



predict()
#fetch_stock_data()

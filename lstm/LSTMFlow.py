from metaflow import FlowSpec, step, Parameter
import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
from sklearn.metrics import mean_squared_error
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class StockPricePredictionFlow(FlowSpec):
    @step
    def start(self):
        self.stock_name='DLF.NS'
        self.next(self.download_data)

    @step
    def download_data(self):
        data = yf.download(self.stock_name, start='2021-09-21', end='2022-09-21')
        self.stock_data = data['Close'].values.reshape(-1, 1)
        #self.stock_time = data['Date'].values.reshape(-1, 1)
        self.next(self.preprocess_data)

    @step
    def preprocess_data(self):
        self.scaler = MinMaxScaler()
        scaled_data = self.scaler.fit_transform(self.stock_data)
        X, y = [], []
        for i in range(len(scaled_data) - 10):
            X.append(scaled_data[i:i+10])
            y.append(scaled_data[i+10])

        self.X = np.array(X)
        self.y = np.array(y)
        print(self.X.shape, self.y.shape, "9999999999")
        self.next(self.train_model)

    @step
    def train_model(self):
    
        # Build the LSTM model
       model = Sequential()
       model.add(LSTM(128, return_sequences=True, input_shape=(10, 1)))
       model.add(Dropout(0.2))
       model.add(LSTM(128))
       model.add(Dropout(0.2))
       model.add(Dense(1)) 

       # Compile the model
       optimizer = Adam(learning_rate=0.001)
       model.compile(optimizer=optimizer, loss='mean_squared_error')
       print("Model compiled")

       self.model = model
       self.next(self.calculate_error)
    #    self.next(self.end)

    @step
    def calculate_error(self):
        self.predictions = self.model.predict(self.X)
        self.error_rate = mean_squared_error(self.y, self.predictions)
        print("Mean Squared Error:", self.error_rate)
        self.next(self.write_to_influx)

    @step
    def write_to_influx(self):
        print(self.predictions.shape)
        print("end==============================")
        transformed_data = self.scaler.inverse_transform(self.predictions)
        transformed_data_y = self.scaler.inverse_transform(self.y)
        print(transformed_data, transformed_data_y)
        
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
        for index, value in np.ndenumerate(transformed_data):
            #print(index[0], value)
            #parsed_time = datetime.strptime(self.stock_time, '%Y-%m-%d %H:%M:%S.%f')
            # Convert the datetime object to nanoseconds
            #nanoseconds = parsed_time.timestamp() * 1e9
            p = influxdb_client.Point("actual_stock").tag("name", self.stock_name).field("price", value) 
            p = influxdb_client.Point("predict_stock").tag("name", self.stock_name).field("price", value) #.time(nanoseconds)
            write_api.write(bucket=bucket, org=org, record=p)
            print('Written to influx')
        self.next(self.end)  

    @step
    def end(self):
        pass

if __name__ == '__main__':
    StockPricePredictionFlow()

# stock_time_series


**
#Installation**

1. Install InfluxDB 

      1. Download curl -O https://download.influxdata.com/influxdb/releases/influxdb2_2.7.6-1_amd64.deb 
                sudo dpkg -i influxdb2_2.7.6-1_amd64.deb
      2.  Start the InfluxDB service   sudo service influxdb start
      3.  To verify the service        sudo service influxdb status
      4.  Opening Influx in browser    http://localhost:8086/

2. Installing Grafana

      1. wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
      2. sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
      3. sudo apt-get install grafana
      4. sudo systemctl start grafana-server
      5. sudo systemctl status grafana-server
      6. sudo systemctl enable grafana-server
      7. open at http://localhost:3000
  
         
4. Install apache kafka
   
   Download     $ tar -xzf kafka_2.13-3.7.0.tgz
                $ cd kafka_2.13-3.7.0
   
   Start the kafka
   
               $ bin/zookeeper-server-start.sh config/zookeeper.properties
   
               $ bin/kafka-server-start.sh config/server.properties
     
3. Installing metaflow
          1. pip install metaflow
   
**#High level Design**

![image](https://github.com/xrcwrn/stock_time_series/assets/5010715/fe98dbfd-c816-4492-9848-6ead284ed941)



**#Outout**

   **Live Stock Price**
   TataSteel Limited
    ![image(1)](https://github.com/xrcwrn/stock_time_series/assets/5010715/39fa0dd8-a2e6-4b54-990a-5f2cc9afaf6b)

   Nifty 50 and DLF
    ![image](https://github.com/xrcwrn/stock_time_series/assets/5010715/d62fd3f2-a92c-4378-b6b6-a0296e89a99a)

   Prediction Analysis on DLF
   ![image](https://github.com/xrcwrn/stock_time_series/assets/5010715/535f0393-48d5-4218-8b92-9a878e6b06c8)





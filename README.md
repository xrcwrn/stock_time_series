# stock_time_series

1. Install InfluxDB 

      1. Download
     
          curl -O https://download.influxdata.com/influxdb/releases/influxdb2_2.7.6-1_amd64.deb
          sudo dpkg -i influxdb2_2.7.6-1_amd64.deb
     
       2.  Start the InfluxDB service
     
               sudo service influxdb start
                
       3.  To verify the service
     
               sudo service influxdb status
     
        
       4.  Opening Influx in browser
     
              http://localhost:8086/

2. Installing Grafana

      1. wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
      2. sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
      3. sudo apt-get install grafana
      4. sudo systemctl start grafana-server
      5. sudo systemctl status grafana-server
      6. sudo systemctl enable grafana-server
     
3. Installing metaflow
       1. pip install metaflow

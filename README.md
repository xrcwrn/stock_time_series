# stock_time_series

Install InfluxDB 

 1. Download

     curl -O https://download.influxdata.com/influxdb/releases/influxdb2_2.7.6-1_amd64.deb
     sudo dpkg -i influxdb2_2.7.6-1_amd64.deb

3. Start the InfluxDB service
   
   sudo service influxdb start
4. To verify the service

   sudo service influxdb status
6. Opening Influx in browser

    http://localhost:8086/

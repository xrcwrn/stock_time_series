from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'stock'})
c.subscribe(['DLF.NS','SBIN.NS','HDFCBANK.NS','RELIANCE.NS','ICICIBANK.NS','INFY.NS','LT.NS','TCS.NS','ITC.NS','AXISBANK.BO','BHARTIARTL.NS'])
msg = c.poll(1.0)

while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print('Error: {}'.format(msg.error()))
        continue
    print('Received message on {}: {}'.format(msg.topic(), msg.value().decode('utf-8')))
    

import bluetooth
 
bd_addr = 'E6:52:28:5E:0C:53' # The address from the SPI adapter
# bd_addr = 'E4:DB:75:D5:D2:AC' # The address from the UART adapter
# bd_addr = "" # Might just need a blank address?
port = 1
backlog = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind((bd_addr,port))
sock.listen(backlog)

data = ""

try:
    client, clientInfo = sock.accept()
    print(clientInfo)while 1:
    data += client.recv(1024)
    data_end = 1 #data.find('\n')
    if data_end != -1:
         rec = data[:data_end]
         print(data)
         data = data[data_end+1:
    else:
         client.close()
except KeyboardInterrupt:
    sock.close()

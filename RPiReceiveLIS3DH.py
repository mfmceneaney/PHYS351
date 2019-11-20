import bluetooth
 
bd_addr = "E6:52:28:5E:0C:53" #The address from the Adafruit Bluefruit LE SPI Friend
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.connect((bd_addr,port)) # Try pairing first to avoid host down error?
 
data = ""
while 1:
	try:
		data += sock.recv(1024)
		data_end = data.find('\n')
		if data_end != -1:
			rec = data[:data_end]
			print data
			data = data[data_end+1:]
	except KeyboardInterrupt:
		break
sock.close()

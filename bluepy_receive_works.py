# Basically, the service you want is the UART service UUID: 6e400001-b5a3-f393-e0a9-e50e24dcca9e
# which has two characteristics, TX (0x0002 for transmit) and RX (0x0003 for receive).  They exchange 20 bytes (each is an 8 bit unsigned integer which can be translated into an ASCII character).
# The python code that I use to do this sort of thing works with bluepy (although I could not get it to connect yesterday):
import ctypes
import binascii
import struct
from bluepy import btle

#class MyDelegate(btle.DefaultDelegate):
#    def __init__(self):
#        btle.DefaultDelegate.__init__(self)
#        # ... initialise here

#    def handleNotification(self, cHandle, data):
#        # ... perhaps check cHandle
 #       print(data)

# This next line is supposed to connect

dev = btle.Peripheral("E4:DB:75:D5:D2:AC","random") # Use your correct address

#dev.withDelegate( MyDelegate() )

print('Services') # This will list the services

for svc in dev.services:
     print(str(svc))

##################################################################################
# For my case, one of the services was f000aa80-0451-4000-b000-000000000000

MovementSensor = btle.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e") # This is unnecessary if you put this address in the line below
#MovementSensor = btle.UUID("00001530-1212-efde-1523-785feabcd123")
print(str(MovementSensor))

MovementService = dev.getServiceByUUID(MovementSensor)
print(str(MovementService))

for ch in MovementService.getCharacteristics(): # This shows the characteristics

     print(str(ch))

##################################################################################
# # These lines are for writing out to the BLE

# # First, some preparation (only necessary once):

# uuidConfig = btle.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e") 

# MovementSensorConfig = MovementService.getCharacteristics(uuidConfig)[0]

# # Now, the actual writing

# MovementSensorConfig.write(struct.pack('H',0x78)) # This is a python 3 way to write out  a byte

##################################################################################
# These lines are for reading in from the BLE

# First, preparation (only necessary once):

#uuidValue  = btle.UUID("00001534-1212-efde-1523-785feabcd123")
uuidValue  = btle.UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e") # This is setting up the read data
# print(str(uuidValue))
print(MovementService.getCharacteristics(uuidValue))
MovementSensorValue = MovementService.getCharacteristics(uuidValue)[0]
# print(str(MovementSensorValue))

#buff = ctypes.create_string_buffer(4)

# Now, the actual read and decoding
# print(str(MovementSensorValue.read()))
# val = struct.unpack("9h",MovementSensorValue.read()) # "9h" (i.e. 9 times and h is for short) refers to the C formatting of the incomming string?
print(MovementSensorValue.supportsRead())
print(MovementSensorValue.propertiesToString())
#while True:
#    if dev.waitForNotifications(1.0):
#        # handleNotification() was called
#        continue
data = ""
while True:
#    print(MovementSensorValue.read(),"\n")
    data += str(MovementSensorValue.read().decode('UTF-8'))
    #data = "".join(c for c in data if c.isdigit())
    print("data0= ", data)
    data_end = data.find("z")
    if data_end != -1:
        #data.replace("\r\n","")
        data = data[data_end + 1:]
        print("data = ",data)
        data_end = data.find("z")
        if data_end != -1:
                toprint = data[:data_end]
                print("toprint = ",toprint) #Frequency Measurement
                data = data[data_end + 1:] 
                #data_end = data.find("\'b\'")
#        data = data[data_end:]
    #print("data = ",data)
    #val = binascii.b2a_hex(MovementSensorValue.read())
    #print(val,"\n")
    #val = binascii.unhexlify(val)
    #print(val,"\n")
    #val = struct.unpack('4f',val)[0]
    # val = struct.unpack_from(MovementSensorValue.read(),buff,0)
    # print(val)
    # print(str(MovementSensorValue))


# Basically, the service you want is the UART service UUID: 6e400001-b5a3-f393-e0a9-e50e24dcca9e
# which has two characteristics, TX (0x0002 for transmit) and RX (0x0003 for receive).  They exchange 20 bytes (each is an 8 bit unsigned integer which can be translated into an ASCII character).
# The python code that I use to do this sort of thing works with bluepy (although I could not get it to connect yesterday):
import time
import binascii
from bluepy import btle

# This next line is supposed to connect

dev = btle.Peripheral("E4:DB:75:D5:D2:AC") # Use your correct address

print('Services') # This will list the services

for svc in dev.services:

     print(str(svc))

##################################################################################
# For my case, one of the services was f000aa80-0451-4000-b000-000000000000

MovementSensor = btle.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e") # This is unnecessary if you put this address in the line below
print(str(MovementSensor))

MovementService = dev.getServiceByUUID(MovementSensor)
print(str(MovementService))

for ch in MovementService.getCharacteristics(): # This shows the characteristics

     print(str(ch))

##################################################################################
# # These lines are for writing out to the BLE

# # First, some preparation (only necessary once):

# uuidConfig = btle.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")

# MovementSensorConfig = MovementService.getCharacteristics(uuidConfig)[0]

# # Now, the actual writing

# MovementSensorConfig.write(struct.pack('H',0x78)) # This is a python 3 way to write out  a byte

##################################################################################
# These lines are for reading in from the BLE

# First, preparation (only necessary once):

uuidValue  = btle.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e") # This is setting up the read data
print(str(uuidValue))

MovementSensorValue = MovementService.getCharacteristics(uuidValue)[0]
print(str(MovementSensorValue))

# Now, the actual read and decoding
print(str(MovementSensorValue.read()))

val = struct.unpack("9h",MovementSensorValue.read()) # "9h" refers to the C formatting of the incomming string?
print(val)

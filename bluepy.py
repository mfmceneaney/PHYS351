#Basically, the service you want is the UART service UUID: 6E400001-B5A3-F393-­E0A9-­E50E24DCCA9E
#which has two characteristics, TX (0x0002 for transmit) and RX (0x0003 for receive). They exchange 20 bytes (each is an 8 bit unsigned integer which can be translated into an ASCII character).
#The python code that I use to do this sort of thing works with bluepy (although I could not get it to connect yesterday):

from bluepy import btle

# This next line is supposed to connect

dev = btle.Peripheral("CC:78:AB:7F:89:02") # Use your correct address

print('Services') # This will list the services

for svc in dev.services:

     print(str(svc))

# For my case, one of the services was f000aa80-0451-4000-b000-000000000000

MovementSensor = btle.UUID("f000aa80-0451-4000-b000-000000000000") # This is unnecessary if you put this address in the line below

MovementService = dev.getServiceByUUID(MovementSensor)

for ch in MovementService.getCharacteristics(): # This shows the characteristics

     print(str(ch))

# These lines are for writing out to the BLE

# First, some preparation (only necessary once):

uuidConfig = btle.UUID("f000aa82-0451-4000-b000-000000000000")

MovementSensorConfig = MovementService.getCharacteristics(uuidConfig)[0]

# Now, the actual writing

MovementSensorConfig.write(struct.pack('H',0x78)) # This is a python 3 way to write out  a byte

# These lines are for reading in from the BLE

# First, preparation (only necessary once):

uuidValue  = btle.UUID("f000aa81-0451-4000-b000-000000000000") # This is seeting up the read data

MovementSensorValue = MovementService.getCharacteristics(uuidValue)[0]

# Now, the actual read and decoding

val = struct.unpack("9h",MovementSensorValue.read())


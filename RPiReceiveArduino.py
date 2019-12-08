# Basically, the service you want is the UART service UUID: 6e400001-b5a3-f393-e0a9-e50e24dcca9e
# which has two characteristics, TX (0x0002 for transmit) and RX (0x0003 for receive).
# They exchange 20 bytes (each is an 8 bit unsigned integer which can be translated into an ASCII character).

from time import time
from bluepy import btle

"""
This module reads the acceleration data from the Bluefruit UART Friend
connected to the Arduino Uno and LIS3DH accelerometer.  It prints measured
accelerations to the screen and allows another program to read the 
measurements and the time they were recieved.
"""

# Global Variable Definitions
acc = 0
t = time()
measurement = [acc,t]
MovementSensor = btle.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e") # UART Service on the Bluefruit

# Function Definitions
def get_acc():
    return measurement

# Main Loop for Receiving Measurements
for i in range(1000000):
     try:
          dev = btle.Peripheral("E4:DB:75:D5:D2:AC","random") # Use your specific address for the BLE device
          MovementService = dev.getServiceByUUID(MovementSensor)
          uuidValue = btle.UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e") # 0x003 is for reading
          MovementSensorValue = MovementService.getCharacteristics(uuidValue)[0]

          print(MovementSensorValue.supportsRead())
          print(MovementSensorValue.propertiesToString())
          
          data = ""
          sensor = MovementSensorValue.read()

          while True:
               data += str(MovementSensorValue.read().decode('UTF-8')) # Make sure this is the actual format of the incoming data
               t = time()
               print("data0= ", data)
               data_end = data.find("z")

               if data_end != -1:
                    data = data[data_end + 1:]
                    print("data = ",data)
                    data_end = data.find("z") # Our Arduino code separates measurements with z

                    if data_end != -1:
                         to_print = data[:data_end]
                         print("toprint = ",toprint)
                         acc = float(to_print)
                         measurement = [acc,t]
                         data = data[data_end + 1:]

     except btle.BTLEDisconnectError:
          print("\nDevice Disconnected...Reconnecting")

     except BrokenPipeError:
          print("\nBroken Pipe...Reconnecting")

     except KeyboardInterrupt:
          print("\nYou have chosen to exit the program")
          break

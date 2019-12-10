# PHYS351
PHYS 351 Scientific Instrumentation Lab Fall 2019 Final Project

## Adafruit LIS3DH 3-axis accelerometer
Download the Arduino library from:
[Adafruit LIS3DH Arduino](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/arduino)

Or clone it with:
```
$ git clone https://github.com/adafruit/Adafruit_LIS3DH.git
```

You must also use the built in Arduino Sensor library.

Documentation for this product is available at:
[Adafruit LIS3DH Triple Axis Accelerometer Breakout](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-lis3dh-triple-axis-accelerometer-breakout.pdf)

## Adafruit Bluefruit Bluetooth LE SPI/UART Friend
Download the library from:

[Adafruit Bluefruit SPI Arduino](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-spi-breakout/software) / [Adafruit Bluefruit UART Arduino](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-uart-friend/software)

Or clone it with:
```
$ git clone https://github.com/adafruit/Adafruit_BluefruitLE_nRF51.git
```

Documentation for these products is available at:

[Introducing the Adafruit Bluefruit SPI](https://cdn-learn.adafruit.com/downloads/pdf/introducing-the-adafruit-bluefruit-spi-breakout.pdf) / [Introducing the Adafruit Bluefruit UART](https://cdn-learn.adafruit.com/downloads/pdf/introducing-the-adafruit-bluefruit-le-uart-friend.pdf)

IMPORTANT: To send data on the UART Friend make sure the on board switch is in UART mode and not CMD mode.

![TestImage](/Images/TeamVaderFlowChart.jpeg)


## Adafruit Pro Trinket 3V Board
Although we did not use it, this has almost the full capabilities of an Arduino Uno board, but is much smaller.  See the documentation at:
[Adafruit Pro Trinket](https://cdn-learn.adafruit.com/downloads/pdf/introducing-pro-trinket.pdf)

To write to the UART Friend you will also need to use the [Arduino SoftwareSerial Library](https://www.arduino.cc/en/Reference/softwareSerial).

To add the board to the Arduino IDE use the directions at [Arduino 1.6x IDE Setup](https://learn.adafruit.com/adafruit-arduino-ide-setup/arduino-1-dot-6-x-ide)

## Raspberry Pi 4 Bluetooth Communication
When using Bluetooth LE on the Raspberry Pi, if the Bluetooth icon is not visible in the top right corner of the screen restart dbus:
```
$ sudo service dbus restart
$ systemctl status dbus.service
```
and you should see something like:
```
● dbus.service - D-Bus System Message Bus
   Loaded: loaded (/lib/systemd/system/dbus.service; static; vendor preset: enabled)
   Active: active (running) since Sat 2019-11-23 12:17:20 EST; 11s ago
     Docs: man:dbus-daemon(1)
 Main PID: 2285 (dbus-daemon)
    Tasks: 1 (limit: 4915)
   Memory: 956.0K
   CGroup: /system.slice/dbus.service
           └─2285 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --syst
```
Then use Bluetoothctl to turn bluetooth on, make the Raspberry Pi discoverable and scan for, pair, and connect to a device and see its UUID and connection information if you know its Mac address:
```
$ bluetoothctl
[bluetoothctl]# power on
[bluetoothctl]# agent on
[bluetoothctl]# default-agent
[bluetoothctl]# discoverable on
[bluetoothctl]# scan on
[bluetoothctl]# pair <device>
[bluetoothctl]# connect <device>
[bluetoothctl]# info <device>
```

## Bluetooth Library BlueZ
This is the software used for bluetooth communication on the Raspberry Pi.  There is not much documentation but the source code API is available here: [BlueZ Source Code](https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/).

To install Bluez software follow the direction at:
[Installing Bluez on the Raspberry Pi](https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation)

## Bluetooth Library Bluepy
This is the python library for Bluetooth LE communication with BlueZ which is automatically installed with BlueZ in Python 2.7 on the Raspberry Pi.  To install Bluepy in Python 3+ use the following commands (after installing BlueZ):
```
sudo apt-get install python3-pip libglib2.0-dev
sudo pip3 install bluepy
```
Also see Ian Harvey's instructions for installing [Bluepy](https://github.com/IanHarvey/bluepy).

To add a the UART Friend as a peripheral make sure to use the "random" option when specifying the Bluetooth LE Address, like so:
```
from bluepy import btle
p = btle.Peripheral("XX:XX:XX:XX:XX:XX","random") # Use your correct address
```
The UART Friend has a base UART service UUID: 6e400001-b5a3-f393-e0a9-e50e24dcca9e.  This has two characteristics: TX (0x0002 for transmit) and RX (0x0003 for receive).  See [Bluefruit UART Service](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-uart-friend/uart-service) for more information.

## Helpful Reading
A great book on Bluetooth programming basics with section on using BlueZ in Python and C:
[An Introduction to Bluetooth Programming, Albert Huang](https://people.csail.mit.edu/albert/bluez-intro/index.html)

Also take a look at this example of bluetooth data transmission between Arduino and Raspberry Pi online:
http://blog.whatgeek.com.pt/2015/09/bluetooth-communication-between-raspberry-pi-and-arduino/

## Further Reading

### Adafruit Bluetooth LE Python Library
For receiving bluetooth data from an Adafruit Bluefruit LE device on the Raspberry Pi download the Adafruit Bluetooth LE Python Library using:
```
$ sudo pip install Adafruit-BluefruitLE
```

Or clone it from gitHub:
```
$ git clone https://github.com/adafruit/Adafruit_Python_BluefruitLE.git
$ cd Adafruit_Python_BluefruitLE
$ sudo python setup.py install
```
Documentation for this is available online at:
[Bluefruit LE Python Library](https://cdn-learn.adafruit.com/downloads/pdf/bluefruit-le-python-library.pdf)


### Bluetooth Python Library PyBluez
For using Bluetooth in python download and install the PyBluez library from:
[PyBluez](https://pypi.org/project/PyBluez/) and follow the instructions for installation on Linux at [PyBluez Documentation](https://pybluez.readthedocs.io/en/latest/install.html).

Or download and install it with:
```
$ pip install PyBluez
```
or for use with Python 3:
```
$ sudo apt-get install bluetooth libbluetooth-dev
$ sudo python3.7 -m pip install pybluez
```
or for BLE dependencies on Linux (just compatible with Python 2):
```
$ sudo apt-get install libboost-python-dev
$ sudo apt-get install libbluetooth-dev
$ pip install pybluez\[ble\]
```
which installs the header files. You might also need to do this for these modules as well:
```
$ sudo apt-get install libboost-thread-dev
$ sudo apt-get install libglib2.0-dev
$ sudo apt-get install python-dev
```
In addition to PyBluez, python has a socket library which can also be used:
http://blog.kevindoran.co/bluetooth-programming-with-python-3/

### Blueman: BlueZ GUI Application
Although we have not had any success using it, you can install Blueman the BlueZ GUI application using:
```
$ sudo dpkg --configure bluez
$ sudo apt-get install bluez blueman
```
and then reboot the Raspberry Pi with:
```
$ sudo reboot
```

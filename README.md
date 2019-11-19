# PHYS351
PHYS 351 Scientific Instrumentation Lab Fall 2019 Final Project

## Adafruit LIS3DH 3-axis accelerometer
Download the Arduino library from:
[Adafruit LIS3DH Arduino](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/arduino)

Or you can clone it with:
```
$ git clone https://github.com/adafruit/Adafruit_LIS3DH.git
```

Documentation for this product is available at:
[Adafruit LIS3DH Triple Axis Accelerometer Breakout](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-lis3dh-triple-axis-accelerometer-breakout.pdf)

## Adafruit Bluefruit Bluetooth LE SPI Friend
Download the library from:
[Adafruit Bluefruit SPI Arduino](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-spi-breakout/software)

Or you can clone it with:
```
$ git clone https://github.com/adafruit/Adafruit_BluefruitLE_nRF51.git
```

Documentation for this product is available at:
[Introducing the Adafruit Bluefruit SPI](https://cdn-learn.adafruit.com/downloads/pdf/introducing-the-adafruit-bluefruit-spi-breakout.pdf)

## Bluetooth Communication
For documentation on the Arduino SoftwareSerial library see:
[Arduino SoftwareSerial Library](https://www.arduino.cc/en/Reference/SoftwareSerial)

For receiving bluetooth data on the Raspberry Pi download the Adafruit Bluetooth LE Python Library using:
```
$ sudo pip install Adafruit-BluefruitLE
```

Or clone it from gitHub:
```
$ git clone https://github.com/adafruit/Adafruit_Python_BluefruitLE.git
$ cd Adafruit_Python_BluefruitLE
$ sudo python setup.py install
```
Documentation is available online at:
[Bluefruit LE Python Library](https://cdn-learn.adafruit.com/downloads/pdf/bluefruit-le-python-library.pdf)

## Bluetooth Python Library
For using Bluetooth in python download and install the PyBluez library from:
[PyBluez](https://pypi.org/project/PyBluez/) and follow the instructions for installation on Linux at [PyBluez Documentation](https://pybluez.readthedocs.io/en/latest/install.html).

Or download and install it with:
```
$ pip install PyBluez
```

or for BLE dependencies on Linux:
```
pip install pybluez\[ble\]
```

Also take a look at this example of bluetooth data transmission between Arduino and Raspberry Pi online:
http://blog.whatgeek.com.pt/2015/09/bluetooth-communication-between-raspberry-pi-and-arduino/

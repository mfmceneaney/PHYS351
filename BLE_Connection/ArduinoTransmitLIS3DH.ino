// General Imports
#include <Arduino.h>
#include <SPI.h>
#include <SoftwareSerial.h>
//  #include <SoftwareSerial.h>
//#endif

// Adafruit Bluefruit LE Imports
#include <Adafruit_ATParser.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include <Adafruit_BLEMIDI.h>
#include <Adafruit_BLEBattery.h>
#include <Adafruit_BLEGatt.h>
#include <Adafruit_BLEEddystone.h>
#include <Adafruit_BLE.h>
#include <Adafruit_BluefruitLE_UART.h>
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"
#include "BluefruitConfig.h"

// Adafruit LIS3DH Imports
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>

// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10

// software SPI
//Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS, LIS3DH_MOSI, LIS3DH_MISO, LIS3DH_CLK);
// hardware SPI
//Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS);
// I2C
Adafruit_LIS3DH lis = Adafruit_LIS3DH();

// MFM 11/18/19
//SoftwareSerial Serial(BLUEFRUIT_SPI_MISO, BLUEFRUIT_SPI_MOSI); // RX, TX

/*=========================================================================
    APPLICATION SETTINGS

? ? FACTORYRESET_ENABLE? ?  Perform a factory reset when running this sketch
? ?
? ?                         Enabling this will put your Bluefruit LE module
                            in a 'known good' state and clear any config
                            data set in previous sketches or projects, so
? ?                         running this at least once is a good idea.
? ?
? ?                         When deploying your project, however, you will
                            want to disable factory reset by setting this
                            value to 0.? If you are making changes to your
? ?                         Bluefruit LE device via AT commands, and those
                            changes aren't persisting across resets, this
                            is the reason why.? Factory reset will erase
                            the non-volatile memory where config data is
                            stored, setting it back to factory default
                            values.
? ? ? ?
? ?                         Some sketches that require you to bond to a
                            central device (HID mouse, keyboard, etc.)
                            won't work at all with this feature enabled
                            since the factory reset will clear all of the
                            bonding data stored on the chip, meaning the
                            central device won't be able to reconnect.
    -----------------------------------------------------------------------*/
    #define FACTORYRESET_ENABLE      1
/*=========================================================================*/


// Create the bluefruit object, either software serial...uncomment these lines

SoftwareSerial bluefruitSS = SoftwareSerial(BLUEFRUIT_SWUART_TXD_PIN, BLUEFRUIT_SWUART_RXD_PIN); //, 

Adafruit_BluefruitLE_UART ble(bluefruitSS, BLUEFRUIT_UART_MODE_PIN,
                      BLUEFRUIT_UART_CTS_PIN, BLUEFRUIT_UART_RTS_PIN);


/* ...or hardware serial, which does not need the RTS/CTS pins. Uncomment this line */
//Adafruit_BluefruitLE_UART ble(BLUEFRUIT_HWSERIAL_NAME, BLUEFRUIT_UART_MODE_PIN);

/* ...hardware SPI, using SCK/MOSI/MISO hardware SPI pins and then user selected CS/IRQ/RST */
//Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

/* ...software SPI, using SCK/MOSI/MISO user-defined SPI pins and then user selected CS/IRQ/RST */
//Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_SCK, BLUEFRUIT_SPI_MISO,
//                             BLUEFRUIT_SPI_MOSI, BLUEFRUIT_SPI_CS,
//                             BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);


// A small helper
void error(const __FlashStringHelper*err) {
  Serial.println(err);
  bluefruitSS.println(err);
  while (1); 
}

/**************************************************************************/
/*!
    @brief  Sets up the HW an the BLE module and the LIS3DH (this function is called
            automatically on startup)
*/
/**************************************************************************/
void setup(void)
{
  // Arduino Serial Monitor comes with a 115200 baud rate.
  Serial.begin(115200);
  // RPi bluetooth comes automatically configured to a 9600 baud rate.
  bluefruitSS.begin(9600);

  //=======================================================================================//
  /* Initialise the Bluefruit module */
  Serial.print(F("Initialising the Bluefruit LE module: "));
//  bluefruitSS.print(F("Initialising the Bluefruit LE module: "));
  
  // These lines have been returning an error
  //if ( !ble.begin(VERBOSE_MODE) )
  //{
  //  error(F("Couldn't find Bluefruit, make sure it's in Command mode & check wiring?"));
  //}
  
  Serial.println( F("OK!") );
//  bluefruitSS.println( F("OK!") );
  
  // Factory Reset has not been working
  //if ( FACTORYRESET_ENABLE )
  //{
  //  /* Perform a factory reset to make sure everything is in a known state */
  //  Serial.println(F("Performing a factory reset: "));
  //  bluefruitSS.println(F("Performing a factory reset: "));
  //  if ( ! ble.factoryReset() ){
  //    error(F("Couldn't factory reset"));
  //  }
  //}
  

  /* Disable command echo from Bluefruit */
  ble.echo(false);

  Serial.println("Requesting Bluefruit info:");
//  bluefruitSS.println("Requesting Bluefruit info:");
  /* Print Bluefruit information through bluefruit module */
  ble.info();
  //=======================================================================================//
  // from acceldemo.c 
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until Serial console opens

  Serial.println("LIS3DH test!");
//  bluefruitSS.println("LIS3DH test!");
  
  if (! lis.begin(0x18)) {   // change this to 0x19 for alternative i2c address
    Serial.println("Couldnt start");
//    bluefruitSS.println("Couldnt start");
    while (1) yield();
  }
  Serial.println("LIS3DH found!");
//  bluefruitSS.println("LIS3DH found!");
  
  lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!
  
  Serial.print("Range = "); Serial.print(2 << lis.getRange());  
  Serial.println("G");
//  bluefruitSS.print("Range = "); bluefruitSS.print(2 << lis.getRange());  
//  bluefruitSS.println("G");
  //=======================================================================================//
}

/**************************************************************************/
/*!
    @brief  Constantly poll for new command and transmit acceleration measurements 
*/
/**************************************************************************/
void loop(void)
{
  // Display command prompt
  //Serial.print(F("AT > "));
  //bluefruitSS.print(F("AT > "));

  // Check for user input and echo it back if anything was found
  //char command[BUFSIZE+1];
  //getUserInput(command, BUFSIZE);

  // Send command
  //ble.println(command);

  // Check response status
  //ble.waitForOK();

  lis.read();      // get X Y and Z data at once
  
  // Print measurements to serial monitor of Arduino
//  Serial.print("X:  "); Serial.print(lis.x); 
//  Serial.print("  \tY:  "); Serial.print(lis.y); 
//  Serial.print("  \tZ:  "); Serial.println(lis.z);

  // Transmit Measurements through Bluefruit module
//  bluefruitSS.print("X:  "); bluefruitSS.print(lis.x); 
//  bluefruitSS.print("  \tY:  "); bluefruitSS.print(lis.y); 
//  bluefruitSS.print("  \tZ:  "); bluefruitSS.print(lis.z);
//  bluefruitSS.println(1.00, HEX);
//  Serial.println(1.00, HEX);

  /* Or....get a new sensor event, normalized */ 
  sensors_event_t event; 
  lis.getEvent(&event);
  
  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.print("\t\tX: "); Serial.print(event.acceleration.x);
//  Serial.print(" \tY: "); Serial.print(event.acceleration.y); 
//  Serial.print(" \tZ: "); Serial.print(event.acceleration.z); 
//  Serial.println(" m/s^2 ");
//  bluefruitSS.println("test");
//  bluefruitSS.println(event.acceleration.z, HEX);
  bluefruitSS.println(lis.z, HEX);
  Serial.println(lis.z);
  // IMPORTANT: Need to put uart friend in command mode, use switch on board or AT commands

  /* Display the results (acceleration is measured in m/s^2) */
//  bluefruitSS.print("\t\tX: "); bluefruitSS.print(event.acceleration.x);
//  bluefruitSS.print(" \tY: "); bluefruitSS.print(event.acceleration.y); 
//  bluefruitSS.print(" \tZ: "); bluefruitSS.print(event.acceleration.z); 
//  bluefruitSS.println(" m/s^2 ");

//  bluefruitSS.println();
//  Serial.println();
 
  delay(10); // time in milliseconds
}

/**************************************************************************/
/*!
    @brief  Checks for user input (via the Serial Monitor)
*/
/**************************************************************************/
void getUserInput(char buffer[], uint8_t maxSize)
{
  memset(buffer, 0, maxSize);
  while( Serial.available() == 0 ) {
    delay(1);
  }

  uint8_t count=0;

  do
  {
    count += Serial.readBytes(buffer+count, maxSize);
    delay(2);
  } while( (count < maxSize) && !(Serial.available() == 0) );
}

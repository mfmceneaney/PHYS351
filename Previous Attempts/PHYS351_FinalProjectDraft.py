import RPi.GPIO as GPIO # load the library
import LIS3DHMOD as acc
# POSSIBLY SOME IMPORT FOR BLUEFRUIT LE SPI FRIEND
import numpy as np
import matplotlib as plt
import time

GPIO.setmode(GPIO.BCM) # Use the Broadcom numbering

# Set up lines to use
GPIO.setup(23, GPIO.IN) # This uses GPIO pin 23 for the input frequency signal from the phase loop
GPIO.setup(12, GPIO.OUT) # This uses GPIO pin 12 for the output driving signal into the motor (duty cycle dependent frequency)
GPIO.setup(14, GPIO.OUT) # This uses GPIO pin 14 for the output signal back into the phase loop (frequency dependent frequency)

# Setup accelerometer
con = acc.LIS3DH()
con.printRegister(con.REG_WHOAMI)

try:
    # Initial assignments
    f_loop = 0
    f_out = 0
    dc_motor = 0
    dc_out = 50
    times = np.zeros(10000)
    accels = np.zeros((3,10000))
    t0 = time.time()
    t_stamp = t0
    n = 0
    positions = [0.15,0.20] # out and in positions for motor (0,90) degrees

    # Setup PWM outputs
    PWMMotor = GPIO.PWM(12, 100)  # channel (pin) = 12, frequency=100Hz -> period=10ms
    PWMOut = GPIO.PWM(14, 10)  # channel (pin) = 14, frequency=100Hz -> period=1ms

    # start up PWM without motor in zeroed position
    PWMOut.start(0)
    PWMMotor.start(positions[1])

    print("Taking data...")
    while(True):
        # Read input frequency from loop (through ADC?)
        loop_in = GPIO.input(23)
        if loop_in != loop_in0:
            t = time.time()
            delta_t = t - t_stamp
            f_loop = 1/(2*delta_t)
            time_stamp = t
            loop_in = loop_in0    
            # Output driving signal to (servo) motor moving it out or back
            dc_motor = positions[loop_in]
            PWMMotor.ChangeDutyCycle(dc_motor)  

        # Measure acceleration
        n += 1
        t = time.time()
        times[n%1000] = t - t0
        accels[0][n%1000] = con.getX()
        accels[1][n%1000] = con.getY()
        accels[2][n%1000] = con.getZ()

        # Calculate pendulum frequency
        min_acc_z = 0.96
        min_t = 0.01
        if accels[2] > min_acc_z and t > min_t:
            delta_t = t - t0
            f_out = 1/(2*delta_t)
            t0 = t
            # Output out signal back into phase loop (through DAC)
            PWMOut.ChangeFrequency(f_out)
            PWMOut.ChangeDutyCycle(dc_out)

# Allow a kill via the keyboard
except KeyboardInterrupt:
        print('Program killed via keyboard')

# this catches ALL other exceptions including errors.  
except:  
    print ("Other error or exception occurred!")

finally:
    PWMMotor.stop()
    PWMOut.stop()
    GPIO.cleanup()
    plt.plot(times,accels[0],'ro'); # plot x
    plt.plot(times,accels[1],'bo'); # plot y
    plt.plot(times,accels[2],'go'); # plot z
    plt.xlabel("time (s)")
    plt.ylabel("acceleration (g)")
    plt.legend(["a_x","a_y","a_z"],loc='best')
    plt.show()
    print("Done")

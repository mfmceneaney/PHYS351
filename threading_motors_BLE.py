from math import math
from time import time
import numpy as np
from queue import Queue 
from threading import Thread
from receive_BLE import receive_BLE
from threading_siri_control import siri_control
from Threading_MotorRunner.py import setup, primary_thread, winddown_fullsteps, windup_fullsteps, swing_fullsteps, swing_halfsteps

"""
Author: Matthew McEneaney
This code should connect to the Adafruit Bluefruit UART Friend to receive accelerations measurements,
check Siri Voice Control and the command line for user input, swing the pendulum and adjust length and 
frequency as requested, and print acceleration measurements and interpreted commands and corresponding
values to the command line. It relies on the function libraries in ~/PHYS351/Threading Libraries/.
Calibration is yet to be performed for interpreting length as a function of motor steps.
"""

# A thread that consumes data 
def consumer(in_q):
    acc0 = 0
    t0 = time()
    length0 = 0
    frequency0 = 1
    while True: 
        # Get some data 
        data = in_q.get()

        # Process the data 
        if data[0] == "measurement":
            print("acc = ",data[1],", t = ",data[2])
            acc = data[1]
            accelerations.append[]
            if abs(acc) > 0.925: # choose an arbitrary threshold
                t = data[2]
                measured_frequency = 1/(t - t0)
                print(measured_frequency)
                t0 = t
            
        if data[0] == "length":
            print("length = ",data[1])
            length = data[1]
            if length > length0:
                winddown_fullsteps(length)
            if length < length0:
                windup_fullsteps(length)
            frequency0 = 2*pi*sqrt(9.81/length)

        if data[0] == "frequency":
            print("frequency = ",data[1])
            frequency0 = data[1]
            length = 9.81*(1/(frequency*2*pi))**2
            if length > length0:
                winddown_fullsteps(length)
            if length < length0:
                windup_fullsteps(length)
            length0 = length

        period = 1/frequency0
        swing_fullsteps(period)
        
            
        
# Create the shared queue and launch both threads
try:
    q = Queue() 
    t1 = Thread(target = consumer, args =(q, )) 
    t2 = Thread(target = receive_BLE, args =(q, ))
    t3 = Thread(target = siri_control, args =(q, ))
    setup()
    t1.start()
    t2.start()
    t3.start()
except KeyboardInterrupt:
    q.join()
    break

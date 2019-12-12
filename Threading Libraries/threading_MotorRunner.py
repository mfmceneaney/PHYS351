
import numpy as np
import RPi.GPIO as GPIO
import time
#Initializing
#Total Height of the apparatus is 22in
#300 steps drops to 5 1/4in
#drops by 16.75in
#200 steps drops to 11.5in
#drops by 10.5in
#200 steps to .2667m
#300 steps to .42545m
#Know it has to go through 0,0
#Steps to length equation: .001406x - .003629 = length
#So inverting: 709.8x + 2.908 = steps
#Pendulum natural frequency is: 2pisqrt(L/g)
#so g(1/2pif)^2 = L
#Steps input has to be an integer
oscillations = 5
bumps = 60
frequency = float(input("What Frequency would you like"))
delay = .005
length = 9.81*(1/(frequency*2*np.pi))**2
steps = int(709.8*length +2.908)
print(steps)
if (steps < 400):
    break
else:
    print("Too Low")
def setup():
    #Turn on GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #Label Pins
    #Motor 1
    coil_1_A_1_pin = 5 #black
    coil_1_A_2_pin = 6 #green
    coil_1_B_1_pin = 9 #red
    coil_1_B_2_pin = 10 #blue
    #Motor 2
    coil_2_A_1_pin = 15#black
    coil_2_A_2_pin = 18#green
    coil_2_B_1_pin = 27#red
    coil_2_B_2_pin = 22#blue
    #Setup Pins
    #Motor 1
    GPIO.setup(coil_1_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_1_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_1_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_1_B_2_pin, GPIO.OUT)
    #Motor 2
    GPIO.setup(coil_2_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_2_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_2_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_2_B_2_pin, GPIO.OUT)
#Initializing Motors
def setStep1(w1, w2, w3, w4): # controls motor 1
    #'''Takes 4 inputs, controls signal sent to coils in Motor 1'''
        GPIO.output(coil_1_A_1_pin, w1)
        GPIO.output(coil_1_A_2_pin, w2)
        GPIO.output(coil_1_B_1_pin, w3)
        GPIO.output(coil_1_B_2_pin, w4)
def setStep2(w1, w2, w3, w4): # controls motor 2
    #'''Takes 4 inputs, controls signal sent to coils in Motor 2'''
        GPIO.output(coil_2_A_1_pin, w1)
        GPIO.output(coil_2_A_2_pin, w2)
        GPIO.output(coil_2_B_1_pin, w3)
        GPIO.output(coil_2_B_2_pin, w4)
#Defining Step Sequences
fullsteps = ((0,1,0,1), (0,1,1,0), (1,0,1,0), (1,0,0,1))
reversefullsteps = ((1,0,0,1), (1,0,1,0), (0,1,1,0), (0,1,0,1))
halfsteps = ((0,1,0,1), (0,1,0,0), (0,1,1,0), (0,0,1,0), (1,0,1,0), (1,0,0,0), (1,0,0,1), (0,0,0,1))
reversehalfsteps = ((0,0,0,1), (1,0,0,1), (1,0,0,0), (1,0,1,0), (0,0,1,0), (0,1,1,0), (0,1,0,0), (0,1,0,1))
def swing_fullsteps(t):
    time.sleep(t)
    if abs(steps > 0 ):
        for i in range(0,abs(steps)):
            for pattern in fullsteps:
                setStep1(*pattern)
                time.sleep(delay)
    #steps = -steps
    if abs(-steps < 0):
        for i in range(0,abs(-steps)):
            for pattern in reversefullsteps:
                setStep1(*pattern)
                time.sleep(delay)
def swing_halfsteps(t):
    # steps = function of length
    time.sleep(t)
    for i in range(0,oscillations):
        for i in range(0,bumps):
            for pattern in halfsteps:
                setStep2(*pattern)
                time.sleep(delay)
        for i in range(0,bumps):
            for pattern in reversehalfsteps:
                setStep2(*pattern)
                time.sleep(delay)
def windup_fullsteps(length):
    # steps = function of length
    if abs(steps > 0 ):
        for i in range(0,abs(steps)):
            for pattern in fullsteps:
                setStep1(*pattern)
                time.sleep(delay)
    def winddown_fullsteps(length):
    # steps = - function of length
    if abs(-steps < 0):
        for i in range(0,abs(-steps)):
            for pattern in reversefullsteps:
                setStep1(*pattern)
                time.sleep(delay)
def windup_halfsteps(length):
    # bumps = function of length
    for i in range(0,bumps):
            for pattern in halfsteps:
                setStep2(*pattern)
                time.sleep(delay)
def winddown_halfsteps(length):
    # bumps = function of length
    for i in range(0,bumps):
        for pattern in reversehalfsteps:
            setStep2(*pattern)
            time.sleep(delay)

def primary_thread():
  pass

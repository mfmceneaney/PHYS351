import RPi.GPIO as GPIO
import time

#variables

delay = 0.0125
steps = 250

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Enable GPIO pins for ENA and ENB for stepper

#enable_a = 18
#enable_b = 22

#Enable pins for IN1-3 to control step sequence
#motor_1
coil_1_A_1_pin = 5 #black
coil_1_A_2_pin = 6 #green
coil_1_B_1_pin = 9 #red
coil_1_B_2_pin = 10 #blue

#motor_2
coil_2_A_1_pin = 15#black
coil_2_A_2_pin = 18#green
coil_2_B_1_pin = 27#red
coil_2_B_2_pin = 22#glue
#Set pin states

#GPIO.setup(enable_a, GPIO.OUT)
#GPIO.setup(enable_b, GPIO.OUT)
#motor_1
GPIO.setup(coil_1_A_1_pin, GPIO.OUT)
GPIO.setup(coil_1_A_2_pin, GPIO.OUT)
GPIO.setup(coil_1_B_1_pin, GPIO.OUT)
GPIO.setup(coil_1_B_2_pin, GPIO.OUT)

#motor_2
GPIO.setup(coil_2_A_1_pin, GPIO.OUT)
GPIO.setup(coil_2_A_2_pin, GPIO.OUT)
GPIO.setup(coil_2_B_1_pin, GPIO.OUT)
GPIO.setup(coil_2_B_2_pin, GPIO.OUT)

#set ENA and ENB to high to enable stepper

#GPIO.output(enable_a, True)
#GPIO.output(enable_b, True)

#function for step sequence

def setStep(w1, w2, w3, w4):
     GPIO.output(coil_1_A_1_pin, w1)
     GPIO.output(coil_1_A_2_pin, w2)
     GPIO.output(coil_1_B_1_pin, w3)
     GPIO.output(coil_1_B_2_pin, w4)
     
     GPIO.output(coil_2_A_1_pin, w1)
     GPIO.output(coil_2_A_2_pin, w2)
     GPIO.output(coil_2_B_1_pin, w3)
     GPIO.output(coil_2_B_2_pin, w4)

#loop through step sequence based on number of steps
fullsteps = ((0,1,0,1), (0,1,1,0), (1,0,1,0), (1,0,0,1))
print("Forward!")
for i in range(0, steps):
    for pattern in fullsteps:
        setStep(*pattern)
        time.sleep(delay)
print("Backward!")
reversefullsteps = ((1,0,0,1), (1,0,1,0), (0,1,1,0), (0,1,0,1))
for i in range(0,steps):
        for pattern in reversefullsteps:
                setStep(*pattern)
                time.sleep(delay)

#Halfsteps
halfsteps = ((0,1,0,1), (0,1,0,0), (0,1,1,0), (0,0,1,0), (1,0,1,0), (1,0,0,0), (1,0,0,1), (0,0,0,1))
for i in range(0,steps):
        for pattern in halfsteps:
                setStep(*pattern)
                time.sleep(delay)



#for i in range(0, steps)
#        fullsteps = ((0,1,0,1), (0,1,1,0), (1,0,1,0), (1,0,0,1))
#print("Forward!")
#for i in range(0, steps):
#    for pattern in fullsteps:
#        setStep(*pattern)
#        time.sleep(delay)
#print("Backward!")
#reversefullsteps = ((1,0,0,1), (1,0,1,0), (0,1,1,0), (0,1,0,1))
#for i in range(0,steps):
#        for pattern in reversefullsteps:
#                setStep(*pattern)
#                time.sleep(delay)

from queue import Queue 
from threading import Thread
from receive_BLE import receive_BLE
from threading_siri_control import siri_control

# A thread that consumes data 
def consumer(in_q):
    while True: 
        # Get some data 
        data = in_q.get()
        # Process the data 
        if data[0] == "measurement":
            print("acc = ",data[1],", t = ",data[2])
        if data[0] == "length":
            print("length = ",data[1])
        if data[0] == "frequency":
            print("frequency = ",data[1])
        
# Create the shared queue and launch both threads 
try:
    q = Queue() 
    t1 = Thread(target = consumer, args =(q, )) 
    t2 = Thread(target = receive_BLE, args =(q, ))
    t3 = Thread(target = siri_control, args =(q, ))
    t1.start()
    t2.start()
    t3.start()
except KeyboardInterrupt:
    q.join()

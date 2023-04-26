import cv2
import socket
import math
import pickle
import sys
import os
import time
import shlex 
import subprocess
import re

max_length = 65000
host = sys.argv[1]
#host = "10.42.0.1"
port = 5000
idx = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sourcehost = "10.42.1.224"
sourcehost = sys.argv[2]
num = 3
sumrt = 0;
Priority = False
while num > 0:
    start =time.time()
    response = os.system("ping -c 1 " + sourcehost)
    if response == 0:
        pingstatus = "Network Active"
        rt = time.time() - start
        sumrt = sumrt + rt
        print(rt)
    else:
        pingstatus = "Network Error"
    num -=1
print("sumrt/3 is {}".format(sumrt/3))
if (sumrt/3) > 0.05:
    Priority = True

#if Priority == False:
#time.sleep(3-sumrt/3)
http = "http://" + sourcehost + ":8081/"
cap = cv2.VideoCapture(http)
#cap = cv2.VideoCapture("http://10.42.1.224:8081/")
ret, frame = cap.read()

while ret:
    # compress frame
    #retval, buffer = cv2.imencode(".jpg", frame)
    retval, buffer = cv2.imencode(".jpg", cv2.flip(frame,1))
    
    # delay for QoS 
   # time.sleep(1-sumrt/3)
    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)

        #frame_info = {"packs":num_of_packs}
        frame_info = {"client":idx, "packs":num_of_packs}
        # send the number of packs to be expected
        print("Number of packs:", num_of_packs)
        if Priority:
            port = 5001
        sock.sendto(pickle.dumps(frame_info), (host, port))
        
        left = 0
        right = max_length

        for i in range(num_of_packs):
            print("left:", left)
            print("right:", right)

            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length
            # send the frames accordingly
            sock.sendto(data, (host, port))
    
    ret, frame = cap.read()

print("done")
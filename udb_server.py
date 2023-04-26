import cv2
import socket
import pickle
import numpy as np
import time
host = "10.42.0.1"
port = 5000
max_length = 65540
dst_host = "10.42.0.122"
d_port = 4000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

frame_info = None
buffer = None
frame = None
client_info = {"client_1":False, "client_2":False, "client_3":False}

print("-> waiting for connection")
flag = 0
while True:
    data, address = sock.recvfrom(max_length)
    #print(address)

    #if flag == 0:
    #    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    sock2.bind((host,4000))
    #    flag += 1

    if len(data) < 100:
        frame_info = pickle.loads(data)

        if frame_info:
            idx = frame_info["client"]
            print(str(address)+ ", idx = " + str(idx))  
            if idx == 1:
                if client_info["client_1"] == False:
                     sock_end_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     sock_end_1.bind((host,4000))
                     client_info["client_1"] = True
                nums_of_packs = frame_info["packs"]
                sock_end_1.sendto(pickle.dumps(frame_info), (dst_host, 4000))
                for i in range(nums_of_packs):
                    data, address = sock.recvfrom(max_length)
                    sock_end_1.sendto(data, (dst_host, 4000))

                    if cv2.waitKey(1) == 27:
                        break
            if idx == 2:
                if client_info["client_2"] == False:
                     sock_end_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     sock_end_2.bind((host,4001))
                     client_info["client_2"] = True
                nums_of_packs = frame_info["packs"]
                sock_end_2.sendto(pickle.dumps(frame_info), (dst_host, 4001))
                for i in range(nums_of_packs):
                    data, address = sock.recvfrom(max_length)
                    sock_end_2.sendto(data, (dst_host, 4001))

                    if cv2.waitKey(1) == 27:
                        break

            if idx == 3:
                if client_info["client_3"] == False:
                     sock_end_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     sock_end_3.bind((host,4002))
                     client_info["client_3"] = True
                nums_of_packs = frame_info["packs"]
                sock_end_3.sendto(pickle.dumps(frame_info), (dst_host, 4002))
                for i in range(nums_of_packs):
                    data, address = sock.recvfrom(max_length)
                    sock_end_3.sendto(data, (dst_host, 4002))

                    if cv2.waitKey(1) == 27:
                        break

print("goodbye")

import time
import socket
import numpy as np
import cv2
import argparse
import logging
from aes import AES
import pdb
import base64
from PIL import Image
UDP_IP = "127.0.0.1"
UDP_PORT = 9505
mode = "ecb"

iteration = 1
print("iteration : {}".format(iteration))

def trans_format_RGB(data):
    #tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.listen(True)


# s = [b'\xff' * 46080 for x in range(20)]
s = [b'\xff' * 19080 for x in range(20)]
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
aes = AES("aes", 256)
start1 = time.time()

aes.key_generation()

end1 = time.time()
print(mode + " key gen {} s".format(end1-start1))

conn, addr = sock.accept()
while True:
    picture = b''

    data = conn.recv(19081)
    conn.send('one'.encode())

    s[data[0]] = data[1:19081]
    print(data[0])
    if data[0] == 19:
        for i in range(20):
            picture += s[i]

        frame = np.fromstring(picture, dtype=np.uint8)
        just_vector = frame
        pdb.set_trace()
        #-------------------------------
        encrypted_vector = picture
        if mode == "ecb":
            start3 = time.time()
            for i in range(iteration):
                decrypted_vector = aes.aes_ecb_decrypt(aes.pad(encrypted_vector))
            end3 = time.time()
        elif mode == "cbc":
            start3 = time.time()
            for i in range(iteration):
                decrypted_vector = aes.aes_cbc_decrypt(encrypted_vector)
            end3 = time.time()
        elif mode == "ofb":
            start3 = time.time()
            for i in range(iteration):
                decrypted_vector = aes.aes_ofb_decrypt(encrypted_vector)
            end3 = time.time()
        just_vector = decrypted_vector
         #-------------------------------
        print(decrypted_vector)
        # imlength = len(picture)
        imlength = 47628
        just_value =trans_format_RGB(just_vector[:imlength])
        pdb.set_trace()
        picture_size = int (np.sqrt((np.array(just_value).size/3)))
        just_array = np.array(just_value).reshape(picture_size, picture_size, 3)
        # opencv_image=cv2.cvtColor(np.array(just_value), cv2.COLOR_RGB2BGR)

        cv2.imwrite("get_tcp.jpg", just_array)
        im = Image.new(mode="RGB", size=(picture_size,picture_size))
        im.putdata(just_value)
        im.save("get_tcp_pil.jpg")
        cv2.imshow("frame", just_array)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


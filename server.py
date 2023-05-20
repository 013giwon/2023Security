import time
import socket
import numpy
import cv2
import argparse
import logging
from aes import AES
import pdb
from PIL import Image
UDP_IP = "127.0.0.1"
UDP_PORT = 9505
mode = "ecb"

iteration = 100
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

org_file = 'Jungkook.png'
img = cv2.imread(org_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(img, 1.3, 5)

im = Image.open(org_file)
# #Convert image data into pixel value bytes
value_vector = im.convert("RGB").tobytes()

imlength = len(value_vector)
# value_vector = frame.convert("RGB").tobytes()
# 
conn, addr = sock.accept()
while True:
    picture = b''
    
    # data = conn.recv(786432)
    # data = conn.recv(46081)
    data = conn.recv(19081)
    conn.send('one'.encode())
    # s[data[0]] = data[1:786432]
    # s[data[0]] = data[1:46081]
    s[data[0]] = data[1:19081]
    print(data[0])
    if data[0] == 19:
        for i in range(20):
            picture += s[i]

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
    # encrypted_vector = picture
        just_vector = picture
    # if mode == "ecb":
    #     start3 = time.time()
    #     for i in range(iteration):
    #         decrypted_vector = aes.aes_ecb_decrypt(aes.pad(encrypted_vector))
    #     end3 = time.time()
    # elif mode == "cbc":
    #     start3 = time.time()
    #     for i in range(iteration):
    #         decrypted_vector = aes.aes_cbc_decrypt(encrypted_vector)
    #     end3 = time.time()
    # elif mode == "ofb":
    #     start3 = time.time()
    #     for i in range(iteration):
    #         decrypted_vector = aes.aes_ofb_decrypt(encrypted_vector)
    #     end3 = time.time()
    # print("key dec {} s".format(end3-start3))
    # value_decrypt = trans_format_RGB(decrypted_vector[:786432])
    

    # value_array = numpy.array(value_decrypt).reshape(512, 512, 3)
        just_value =trans_format_RGB(just_vector)

        pdb.set_trace()
        picture_size = int (numpy.sqrt((numpy.array(just_value).size/3)))
        just_array = numpy.array(just_value).reshape(picture_size, picture_size, 3)
        cv2.imwrite("dec_tcp.jpg", just_array)
        cv2.imshow("frame", just_array)
    # out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


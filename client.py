import socket
import cv2
import time
from PIL import Image
from aes import AES
import numpy as np
import logging
import pdb
from patches import patches

UDP_IP = '127.0.0.1'
UDP_PORT = 9505
mode ="ecb"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.SOCK_DGRAM)
#UDP인경우 생략, TCP는 해주어야 함
sock.connect((UDP_IP, UDP_PORT))


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
org_file = 'Jungkook.png'
img = cv2.imread(org_file)
aes = AES("aes", 256)
start1 = time.time()

aes.key_generation()

end1 = time.time()
print(mode + " key gen {} s".format(end1-start1))
def trans_format_RGB(data):
    #tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels

while True:
    # ret, frame = cap.read()
    time.sleep(2)
    # faces = face_cascade.detectMultiScale(img, 1.3, 5)
    # for (x,y,w,h) in faces:
    #     img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #     roi_color = img[y:y+h, x:x+w]
    #     cv2.imwrite("target.jpg", roi_color)
    #     print("image size {}".format(img.size))
    #     filename = "target.jpg"
    #     im = Image.open(filename)
        # roi_color = Image.fromarray(numpy.uint8(roi_color))    
    # value_vector = roi_color.convert("RGB").tobytes()
    filename = "target.jpg"
    im = Image.open(filename)


    
    value_vector = im.convert("RGB").tobytes()
    imlength = len(value_vector)
    # if mode == "ecb":
    #     start2 = time.time()
    #     encrypted_vector = aes.aes_ecb_encrypt(aes.pad(value_vector))
    #     end2 = time.time()
    # elif mode == "cbc":
    #     start2 = time.time()
    #     encrypted_vector = aes.aes_cbc_encrypt(aes.pad(value_vector))
    #     end2 = time.time()
    # elif mode == "ofb":
    #     start2 = time.time()
    #     encrypted_vector = aes.aes_ofb_encrypt(aes.pad(value_vector))
    #     end2 = time.time()

    # print("key enc {} s".format(end2-start2))
    # # 
    # value_encrypt = trans_format_RGB(encrypted_vector[:imlength])
    value_vector = trans_format_RGB(value_vector[:imlength])
    # logging.info("value_encrypt: {}".format(value_encrypt))
    # im2 = Image.new(im.mode, im.size)
    # im2.putdata(value_encrypt)
    # value_encrypt = np.array(value_encrypt)
    value_vector = np.array(value_vector)
    # d = value_encrypt.flatten()
    d = value_vector.flatten()
    s = d.tostring()

    for i in range(20):
        sock.sendto(bytes([i]) + s[i * 19080:(i + 1) * 19080], (UDP_IP, UDP_PORT))
        # sock.sendto(bytes([i]) + s[i * 46080:(i + 1) * 46080], (UDP_IP, UDP_PORT))
        # sock.send(bytes([i]) + s[i * 786431:(i + 1) * 786431])
        resp = sock.recv(1024) #서버로부터 답신

        print(resp.decode())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # sock.sendto(value_encrypt, (UDP_IP, UDP_PORT))
#https://awakening95.tistory.com/1
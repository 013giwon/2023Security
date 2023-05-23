import socket
import cv2
import time
from PIL import Image
from aes import AES
import numpy as np
import logging
import pdb
# from patches import patches

TCP_IP = '127.0.0.1'
TCP_PORT = 9505
mode ="ecb"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.SOCK_DGRAM)
#UDP인경우 생략, TCP는 해주어야 함
sock.connect((TCP_IP, TCP_PORT))


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
org_file = 'Jungkook.png'
img = cv2.imread(org_file)
aes = AES("aes", 256)
iteration = 1
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

    filename = "target.jpg"
    im = Image.open(filename)
    
    value_vector = im.convert("RGB").tobytes()
    print(len(value_vector))
    imlength = len(value_vector)
    # pdb.set_trace()
 #-------------------------------
    if mode == "ecb":
        start2 = time.time()
        encrypted_vector = aes.aes_ecb_encrypt(aes.pad(value_vector))
        end2 = time.time()
    elif mode == "cbc":
        start2 = time.time()
        encrypted_vector = aes.aes_cbc_encrypt(aes.pad(value_vector))
        end2 = time.time()
    elif mode == "ofb":
        start2 = time.time()
        encrypted_vector = aes.aes_ofb_encrypt(aes.pad(value_vector))
        end2 = time.time()
    # value_encrypt = trans_format_RGB(encrypted_vector[:imlength])
    value_encrypt = np.array(encrypted_vector)
    d = value_encrypt.flatten()
    s = d.tostring()
    pdb.set_trace()
    # ssss = np.fromstring(s, dtype=np.uint8)
    # im = Image.new(mode="RGB", size=(int(np.sqrt(len(ssss)/3)),int(np.sqrt(len(ssss)/3))))
    # im.putdata(ssss)
    encrypted_vector = s #im.convert("RGB").tobytes()
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
    ##value_vector = np.array(value_vector)
    ##d = value_vector.flatten()
    
   

    for i in range(20):
        sock.sendto(bytes([i]) + s[i * 19080:(i + 1) * 19080], (TCP_IP, TCP_PORT))

        resp = sock.recv(1024) #서버로부터 답신

        print(resp.decode())

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break


        #-------------------------------
        
    pdb.set_trace()
    # imlength = len(picture)
    just_value =trans_format_RGB(just_vector[:imlength])
    pdb.set_trace()
    picture_size = int (np.sqrt((np.array(just_value).size/3)))
    just_array = np.array(just_value).reshape(picture_size, picture_size, 3)
    # opencv_image=cv2.cvtColor(np.array(just_value), cv2.COLOR_RGB2BGR)

    cv2.imwrite("client_tcp_dec_cv2.jpg", just_array)
    im = Image.new(mode="RGB", size=(picture_size,picture_size))
    im.putdata(just_value)
    im.save("client_tcp_dec_pil.jpg")
    # sock.sendto(value_encrypt, (TCP_IP, TCP_PORT))
#https://awakening95.tistory.com/1
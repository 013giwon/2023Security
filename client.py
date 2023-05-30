import socket
import cv2
import time
from PIL import Image
from aes import AES
import numpy as np
import logging
import pdb
from patches import Patches
import sys 
import random

def trans_format_RGB(data):
    #tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels
TCP_IP = '127.0.0.1'
TCP_PORT = 5959
mode = sys.argv[1]
bit_error = int(sys.argv[2])
stride = 21
patch_size = 21
pdb.set_trace()
stride = int(sys.argv[3])
patch_size = int(sys.argv[4])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.SOCK_DGRAM)
#UDP인경우 생략, TCP는 해주어야 함
sock.connect((TCP_IP, TCP_PORT))


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
org_file = 'Jungkook.jpg'
img = cv2.imread(org_file)
# img = Image.open(org_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(img, 1.3, 5)
aes = AES("aes", 256)
iteration = 1
start1 = time.time()

aes.key_generation()
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_color = img[y:y+h, x:x+w]
pdb.set_trace()
cv2.imwrite("target_face.jpg", roi_color)

patch = Patches()

for f in range (1):
    # ret, frame = cap.read()
    time.sleep(2)
    # get image
    filename = "target_face.jpg"
    original_img = Image.open(filename)
    
    # patch generation
    img_patched, img_num_pos= patch.patch_generation(original_img, stride, patch_size) 

    pdb.set_trace() # img_num_pos check

    picture_size = int (np.sqrt((np.array(img_patched).size/3)))
    im = trans_format_RGB(img_patched.flatten())
    im2 = Image.new(mode="RGB", size=(picture_size,picture_size))
    im2.putdata(im)
    im2.save("client_img_patched_" + str(patch_size) + ".jpg") 
    value_vector_o = img_patched.tobytes() # encrypted patch images
    pdb.set_trace()

    random_bytes = random.randint(2,len(value_vector_o))
    if bit_error == True:
        if value_vector_o[random_bytes]%2 == 0:
            replace_num = value_vector_o[random_bytes] + 1
        else:
            replace_num = value_vector_o[random_bytes] -1
        print(bin(value_vector_o[random_bytes]))
        print(bin(replace_num))
        value_vector = value_vector_o[0:random_bytes]  + bytes([replace_num]) + value_vector_o[random_bytes+1:]
    else:
        value_vector = value_vector_o

    imlength = len(value_vector)

    # image encryption
    if mode == "ecb":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector = aes.aes_ecb_encrypt(aes.pad(value_vector))
        end2 = time.time()
    elif mode == "cbc":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector = aes.aes_cbc_encrypt(aes.pad(value_vector))
        end2 = time.time()
    elif mode == "ofb":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector = aes.aes_ofb_encrypt(aes.pad(value_vector))
        end2 = time.time()
    elif mode == "cfb":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector = aes.aes_cfb_encrypt(aes.pad(value_vector))
        end2 = time.time()
        
    print("enc time picture {}".format(end2-start2))
    value_encrypt = np.array(encrypted_vector)
    d = value_encrypt.flatten()
    s = d.tostring()


    encrypted_vector = s
    shuffle_key = [imlength, np.array(original_img).shape[0], np.array(original_img).shape[1], stride, patch_size]
    for i in img_num_pos:
        shuffle_key.append(i[2])
    pdb.set_trace()

    shuff_key_byte = bytes(str(shuffle_key), 'utf-8')
 
    # key encryption
    if mode == "ecb":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector2 = aes.aes_ecb_encrypt(aes.pad(shuff_key_byte))
        end2 = time.time()
    elif mode == "cbc":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector2 = aes.aes_cbc_encrypt(aes.pad(shuff_key_byte))
        end2 = time.time()
    elif mode == "ofb":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector2 = aes.aes_ofb_encrypt(aes.pad(shuff_key_byte))
        end2 = time.time()
    elif mode == "cfb":
        start2 = time.time()
        for i in range(iteration):
            encrypted_vector2 = aes.aes_cfb_encrypt(aes.pad(shuff_key_byte))
        end2 = time.time()
    print("enc time key {}".format(end2-start2))
    print('=======key in client=======')
    print(shuff_key_byte)
    
    for i in range(20):
        sock.sendto(bytes([i]) + s[i * 19080:(i + 1) * 19080], (TCP_IP, TCP_PORT))
        resp = sock.recv(1024) #서버로부터 답신
        print(resp.decode())

    value_encrypt2 = np.array(encrypted_vector2)
    d_key = value_encrypt2.flatten()
    s_key = d_key.tostring()
    if resp.decode() == "please send the shuffle key":
        print("key send now!")

        sock.sendto(bytes([20]) + s_key , (TCP_IP, TCP_PORT))
        #-------------------------------
        
#https://awakening95.tistory.com/1
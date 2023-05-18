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
mode = "ofb"

iteration = 100
print("iteration : {}".format(iteration))
def trans_format_RGB(data):
    #tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(20)]

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))
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
# for (x,y,w,h) in faces:
#     img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#     roi_gray = img[y:y+h, x:x+w]
#     roi_color = img[y:y+h, x:x+w]

# cv2.imwrite("facedetect.jpg", img)
# cv2.imwrite("target.jpg", roi_color)
cv2.imwrite("Jungkook.jpg", img)
print("image size {}".format(img.size))
# filename = "target.jpg"
filename = "Jungkook.jpg"
im = Image.open(filename)
# #Convert image data into pixel value bytes
value_vector = im.convert("RGB").tobytes()

imlength = len(value_vector)
# value_vector = frame.convert("RGB").tobytes()
# 
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

print("key enc {} s".format(end2-start2))
# pdb.set_trace()
value_encrypt = trans_format_RGB(encrypted_vector[:imlength])

logging.info("value_encrypt: {}".format(value_encrypt))
im2 = Image.new(im.mode, im.size)
im2.putdata(value_encrypt)
filename_encrypted = "target_enc_" + mode + org_file[:5] + ".jpg"
# # Save the object as an image in the corresponding format
im2.save(filename_encrypted)
# pdb.set_trace()
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
print("key dec {} s".format(end3-start3))
value_decrypt = trans_format_RGB(decrypted_vector[:imlength])

im3 = Image.new(im.mode, im.size)
im3.putdata(value_decrypt)
filename_encrypted_dec = "target_dec_" + mode + org_file[:5] + ".jpg"
# # Save the object as an image in the corresponding format
im3.save(filename_encrypted_dec)

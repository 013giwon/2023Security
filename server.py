
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
aes.key_generation()
org_file = 'Jungkook.png'
img = cv2.imread(org_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(img, 1.3, 5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = img[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

cv2.imwrite("facedetect.jpg", img)
cv2.imwrite("target.jpg", roi_color)
filename = "target.jpg"
im = Image.open(filename)
# #Convert image data into pixel value bytes
value_vector = im.convert("RGB").tobytes()

imlength = len(value_vector)
# value_vector = frame.convert("RGB").tobytes()
# encrypted_vector = aes.aes_ecb_encrypt(aes.pad(value_vector))

encrypted_vector = aes.aes_ecb_encrypt(aes.pad(value_vector))

# pdb.set_trace()
value_encrypt = trans_format_RGB(encrypted_vector[:imlength])

logging.info("value_encrypt: {}".format(value_encrypt))
im2 = Image.new(im.mode, im.size)
im2.putdata(value_encrypt)
filename_encrypted = "target_enc_" + mode + org_file[:5] + ".jpg"
# # Save the object as an image in the corresponding format
im2.save(filename_encrypted)
# pdb.set_trace()
decrypted_vector = aes.aes_ecb_decrypt(aes.pad(encrypted_vector))
value_decrypt = trans_format_RGB(decrypted_vector[:imlength])
im3 = Image.new(im.mode, im.size)
im3.putdata(value_decrypt)
filename_encrypted_dec = "target_dec_" + mode + org_file[:5] + ".jpg"
# # Save the object as an image in the corresponding format
im3.save(filename_encrypted_dec)

# plaintext = aes.decryption(ciphertext=ciphertext)
# logging.info("plaintext: {}".format(plaintext))
# while True:
#     picture = b''

#     data, addr = sock.recvfrom(46081)
#     s[data[0]] = data[1:46081]

#     if data[0] == 19:
#         for i in range(20):
#             picture += s[i]

#         frame = numpy.fromstring(picture, dtype=numpy.uint8)
#         #frame = frame.reshape(480, 640, 3)
#         # cv2.imshow("frame", frame)
#         # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         # #cv2.imshow("frame", frame)
#         # for (x,y,w,h) in faces:
#         #     frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
#         #     # roi_gray = gray[y:y+h, x:x+w]
#         #     frame = frame[y:y+h, x:x+w]
#         cv2.imshow("frame", frame)
#         #     frame2 = frame.reshape(-1,)
#         #   #  pdb.set_trace()
#         # #rsa.print_keypair()
#         #     # sssize = frame.shape
#         #     ciphertext = aes.encryption(plaintext=frame2[:10])
            
#         #     logging.info("ciphertext: {}".format(ciphertext))
#         #     plaintext = aes.decryption(ciphertext=ciphertext)
#         #     logging.info("plaintext: {}".format(plaintext))
#         # out.write(frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break

#             #https://awakening95.tistory.com/1

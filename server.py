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
from patches import Patches
import sys
import random



def trans_format_RGB(data):
    #tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels

def main(args):
    pdb.set_trace()
    TCP_IP = args.addr
    TCP_PORT = int(args.port)
    mode = args.mode
    bit_error = int(args.bit_error) 
    iteration = 1000
    print("iteration : {}".format(iteration))


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #socket.SOCK_DGRAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(True)

    s = [b'\xff' * 19080 for x in range(20)]
    key_byte = [b'\xff' * 19080 for x in range(21)]

    aes = AES("aes", 256)
    start1 = time.time()

    aes.key_generation()

    end1 = time.time()
    # print(mode + " key gen {} s".format(end1-start1))

    conn, addr = sock.accept()
    while True:
        picture = b''
        data = conn.recv(19081)
        
        if data[0] < 19: 
            conn.send(str(data[0]).encode())
        key_byte[data[0]] = data[1:19081]
        
        if data[0] == 19:
            for i in range(20):
                picture += key_byte[i]

            frame = np.fromstring(picture, dtype=np.uint8)
            just_vector = frame
            conn.send('please send the shuffle key'.encode())

            # image decryption
            value_vector_o = picture

            random_bytes = random.randint(2,len(value_vector_o))
            if bit_error == True:
                if value_vector_o[random_bytes]%2 == 0:
                    replace_num = value_vector_o[random_bytes] + 1
                else:
                    replace_num = value_vector_o[random_bytes] -1
                print(bin(value_vector_o[random_bytes]))
                print(bin(replace_num))
                encrypted_vector = value_vector_o[0:random_bytes]  + bytes([replace_num]) + value_vector_o[random_bytes+1:]
            else:
                encrypted_vector = value_vector_o

            if mode == "ecb":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_ecb_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()
            elif mode == "cbc":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_cbc_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()
            elif mode == "ofb":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_ofb_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()
            elif mode == "cfb":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_cfb_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()

            print("dec time picture {}".format(end3-start3))
            just_vector = decrypted_vector
            
            
        # shuffle key decryption
        if data[0] == 20:
            key = key_byte[data[0]]
            key_len = data[-1]

            encrypted_vector = key #key[:10]
            if mode == "ecb":
                start3 = time.time()
                for i in range(iteration):
        
                    decrypted_vector = aes.aes_ecb_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()
            elif mode == "cbc":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_cbc_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()
            elif mode == "ofb":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_ofb_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()
            elif mode == "cfb":
                start3 = time.time()
                for i in range(iteration):
                    decrypted_vector = aes.aes_cfb_decrypt(aes.pad(encrypted_vector))
                end3 = time.time()

            print("dec time key {}".format(end3-start3))
            pdb.set_trace()
            dec_shuffle_key = decrypted_vector.decode('utf-8')

            dec_shuff_k = dec_shuffle_key[1:-1].split(',')
            
            img_size = int(dec_shuff_k[0])
            img_h = int(dec_shuff_k[1])
            img_w = int(dec_shuff_k[2])
            patch_size = int(dec_shuff_k[4])
            shuff_key_list = [] 
            total =  (img_h // (patch_size)) * (img_w // (patch_size))
            for i in range(total + 5 - 1):
                shuff_key_list.append(int(dec_shuff_k[i].strip()))
            pdb.set_trace()
            shuff_key_list.append(int(dec_shuff_k[5+total-1].split(']')[0]))

            imlength = shuff_key_list[0]
            just_value =trans_format_RGB(just_vector[:imlength])
            picture_size = int (np.sqrt((np.array(just_value).size/3)))
            just_array = np.array(just_value).reshape(picture_size, picture_size, 3)

            im = Image.new(mode="RGB", size=(picture_size,picture_size))
            im.putdata(just_value)
            im.save("get_tcp_shuffled.jpg")      
            # patches reconstruction 
            patch = Patches()
            img = patch.patch_reconst(shuff_key_list[3:], just_array) 
            pdb.set_trace()    

            rec_value =trans_format_RGB(img.flatten())
            im2 = Image.new(mode="RGB", size=(picture_size,picture_size))
            im2.putdata(rec_value)
            im2.save("pil_tcp_reconstructed_" + mode + ".jpg") 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, default='ecb',
                        help='AES ecb/cbc/cfb/ofb.')
    parser.add_argument('-e', '--bit_error', type=str, default='0',
                        help=' 0 : normal 1 :one-bit error')
    parser.add_argument('-p', '--port', type=str, default='5959',
                        help='TCP port.')
    parser.add_argument('-a', '--addr', type=str, default='127.0.0.1',
                        help='TCP addr.')
    args = parser.parse_args()
    main(args)

    #python server.py -m ecb -p 5959 -e 0
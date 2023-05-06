import base64
from algorithm import Algorithm
from Crypto.Cipher import AES as AESL
import os
BLOCK_SIZE = 16

class AES(Algorithm):
    def __init__(self, name, klen):
        super().__init__(name)
        self.params["klen"] = klen
        self.asymmetric = False

    def key_generation(self, **kwargs):
        klen = self.params["klen"]
        kbytes = (int)(klen/8)
        #key = open("/dev/urandom", "rb").read(kbytes)
        key =  os.urandom(kbytes)
        self.keypair["private"] = key

    def print_keypair(self):
        private = self.keypair["private"].export_key()
        print ("Print {}'s keypair ===".format(self.name))
        print (" - private key: {}".format(private))
    def pad(self, data):
        return data + b"\x00" * (16 - len(data) % 16)
    def encryption(self, **kwargs):
        if not "plaintext" in kwargs:
            encrypted = None
        else:
            plaintext = kwargs["plaintext"]
            pad = BLOCK_SIZE - len(plaintext)
            msg = plaintext + pad * chr(pad)
            iv = "0" * 16
            key = self.keypair["private"]
            aes = AESL.new(key, AESL.MODE_CBC, iv.encode())
            encrypted = base64.b64encode(aes.encrypt(msg.encode())).decode()
        return encrypted
    def aes_ecb_encrypt(self, data, mode=AESL.MODE_ECB):
        #The default mode is ECB encryption
        key = self.keypair["private"]
        aes = AESL.new(key, mode)
        new_data = aes.encrypt(data)
        return new_data
    def decryption(self, **kwargs):
        if not "ciphertext" in kwargs:
            decrypted = None
        else:
            ciphertext = kwargs["ciphertext"]
            iv = "0" * 16
            key = self.keypair["private"]
            aes = AESL.new(key, AESL.MODE_CBC, iv.encode())
            decrypted = aes.decrypt(base64.b64decode(ciphertext)).decode()
            decrypted = decrypted[0:-ord(decrypted[-1])]
        return decrypted

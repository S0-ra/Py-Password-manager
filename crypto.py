import os
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend

SALT_FILE='salt.bin'

def get_or_create_salt():
    #Retrive salt(seed value to generate keys) or bin or generate one
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE,'rb') as file:
            return file.read()
    else:
        salt=os.urandom(16)
        with open(SALT_FILE,'wb') as file:
            file.write(salt)
    
    return salt


def generate_key(master_password):
    #Uses master password and salt value to generate a unique key value
    salt=get_or_create_salt()
    kdf=PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, #32 bytes as AES-256 uses a 256 bit key size
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

def encrypt_password(key,plaintext_password):
    iv=os.urandom(16)
    cipher=Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())
    encrpytor=cipher.encryptor()
    padded_password=plaintext_password+" "*(16-len(plaintext_password)%16)
    encrypted_password=encrpytor.update(padded_password.encode())+encrpytor.finalize()
    return base64.b64encode(iv+encrypted_password).decode()

def decrypt_passowrd(key,encrypted_password):
    encrypted_password=base64.b64decode(encrypted_password)
    iv,cipher_text=encrypted_password[:16],encrypted_password[16:]
    cipher=Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())
    decryptor=cipher.decryptor()
    decrypted_password=decryptor.update(cipher_text)+decryptor.finalize()
    return decrypted_password.decode().strip()
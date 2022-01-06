"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Text encyption and decryption functions
"""

import os
from dotenv import load_dotenv, find_dotenv
from cryptography.fernet import Fernet

load_dotenv(find_dotenv())
key = os.getenv('CYPHER_TOKEN')

def encFile(filename):
    '''This function encrypts the file'''
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(filename, 'rb') as file:
        original = file.read()
        
    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decFile(filename):
    '''This function decrypts the file'''
    fernet = Fernet(key)

    # opening the encrypted file
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)

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


def encMess(message):
    '''Fucntion to encrypt the provided message'''

    hawkEye =   Fernet(key)                            # Reference
    resEnc  =   hawkEye.encrypt(message.encode())      # Encryting the encoded message
    return resEnc


def decMess(message):
    '''Function to decrypt the provided message'''

    hawkEye =   Fernet(key)                            # Reference
    resDec  =   (hawkEye.decrypt(message)).decode()    # Decrypting and decoding the message
    return resDec
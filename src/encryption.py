# For password encryption when I add that feature

import os
import json

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import requests
from requests import Response

salt = b"=\x9a\xcc\xe8\xd2\x9c\x97c\x97?(|\xaa\xd1\x98S)\xe8\x9cL\xed\x90\xa6\xc2\x07\xb5\x9d\xf7C=\xf7\x87\x11SHR\xcaou\xe2\x10\x91\xadN\x17'\x1b\xc7v3\x18\xbc\xa0?X\xbe\xb7X\xa5\xf6\xf3\xdf\xac\xa7"
password = os.getenv("EncryptionKey") or "werfgjiklohui4f5toyj9534ft"
key = PBKDF2(password, salt, dkLen=32)


def encrypt(filename, message):

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(message, AES.block_size))

    with open(filename, "wb") as f:
        f.write(cipher.iv)
        f.write(ciphered_data)

    return ciphered_data


def decrypt(filename):
    with open(filename, "rb") as f:
        iv = f.read(16)
        decrypt_data = f.read()

    # cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_password = cipher.decrypt(decrypt_data)
    unpadded_password = unpad(decrypted_password, AES.block_size)
    password = unpadded_password.decode("utf-8")

    return password


def decrypt_response_content(response: Response):
    response.apparent_encoding
    parsed = json.loads(response.content.decode(response.encoding))
    return parsed

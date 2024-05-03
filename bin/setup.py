import random
import os
import sys
from dotenv import load_dotenv, find_dotenv

from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

load_dotenv(find_dotenv())

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@!$^*+-/?'
chars = list(chars)
random.shuffle(chars)
chars = ''.join(chars)

env_content = '''{{
    EncryptionKey={EncryptionKey}
}}'''.format(EncryptionKey=chars)

with open('../.env', 'w') as f:
    f.write(env_content)
    f.close()

salt = b"=\x9a\xcc\xe8\xd2\x9c\x97c\x97?(|\xaa\xd1\x98S)\xe8\x9cL\xed\x90\xa6\xc2\x07\xb5\x9d\xf7C=\xf7\x87\x11SHR\xcaou\xe2\x10\x91\xadN\x17'\x1b\xc7v3\x18\xbc\xa0?X\xbe\xb7X\xa5\xf6\xf3\xdf\xac\xa7"
encryptionkey = os.getenv('EncryptionKey') or "werfgjiklohui4f5toyj9534ft"
print(encryptionkey)
key = PBKDF2(encryptionkey, salt, dkLen=32)

iv = get_random_bytes(16)
padded_password = pad(sys.argv[1].encode('utf-8'), AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
encrypted_password = cipher.encrypt(padded_password)

with open('../auth.bin', 'wb') as f:
    f.write(iv)
    f.write(encrypted_password)
    f.close()
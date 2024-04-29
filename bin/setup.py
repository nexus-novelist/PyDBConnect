import random
import string

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@!$^*+-/?'
chars = list(chars)
random.shuffle(chars)
chars = ''.join(chars)

env_content = '''{{
    EncryptionKey={EncryptionKey}
}}'''.format(EncryptionKey=chars)

with open('../.env', 'w') as f:
    f.write('')
    f.write(env_content)
    f.close()
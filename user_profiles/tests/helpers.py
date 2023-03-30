from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from mysecrets import SALT


def encrypt_email(email, key=SALT):
    key = key.encode('utf-8')
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_email = pad(email.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_email)
    encrypted_email = iv + ciphertext
    return encrypted_email

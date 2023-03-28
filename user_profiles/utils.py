from Crypto.Cipher import AES
from base64 import b64decode
from secrets import SALT
import hashlib


def decrypt_email(encrypted_email, salt=SALT):
    key = hashlib.sha256(salt.encode()).digest()
    cipher = AES.new(key, AES.MODE_EAX, b64decode(encrypted_email)[:16])
    decrypted = cipher.decrypt(b64decode(encrypted_email)[16:])
    return decrypted.decode('utf-8')
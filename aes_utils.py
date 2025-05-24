
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def pad(text):
    return text + (16 - len(text) % 16) * chr(16 - len(text) % 16)

def unpad(text):
    return text[:-ord(text[-1:])]

def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt(raw, password):
    raw = pad(raw)
    key = get_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

def decrypt(enc, password):
    enc = base64.b64decode(enc)
    key = get_key(password)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]).decode('utf-8'))

import os
from cryptography.fernet import Fernet
import base64
import hashlib

PROTECTED_ENDPOINTS = [
    os.environ.get('CHECK_ADMIN_URL'),
    os.environ.get('VALIDATE_URL'),
    os.environ.get('REGISTER_URL'),
    os.environ.get('LOGIN_URL'),
    os.environ.get('DELETE_POST'),
    os.environ.get('UPLOAD_POST'),
    os.environ.get('POSTS_REACTIONS'),
    os.environ.get('EDIT_POST'),
    os.environ.get('CHECK_PASSWORD'),
    os.environ.get('EDIT_PROFILE'),
    os.environ.get('GET_NEW_ACCESSTOKEN'),
    os.environ.get('DELETE_ACCOUNT'),
    os.environ.get('USER_POST_INFO'),
    os.environ.get('POST_VIEWS')
]

PUBLIC_ENDPOINTS = [
    os.environ.get('GET_POSTS_URL'),
    os.environ.get('GET_LATEST_POST_URL'),
    os.environ.get('USER_LIKED'),
    os.environ.get('LIKE_POST'),
    os.environ.get('UNLIKE_POST'),
    os.environ.get('USER_REACTIONS'),
    os.environ.get('ADD_REACTION'),
    os.environ.get('REM_REACTION'),
    os.environ.get('MOST_LIKED'),
    os.environ.get('MOST_VIEWED')
]

def generate_key(key_str):
    key_bytes = hashlib.sha256(key_str.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)

def encrypt_string(key, message):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_string(key, encrypted_message):
    fernet = Fernet(key)
    try:
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception:
        return None
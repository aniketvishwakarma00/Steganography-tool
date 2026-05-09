from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

# Generate 32-byte key from password
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

# Encrypt message
def encrypt_message(message, password):
    key = generate_key(password)

    cipher = AES.new(key, AES.MODE_CBC)

    encrypted_bytes = cipher.encrypt(
        pad(message.encode(), AES.block_size)
    )

    encrypted_data = base64.b64encode(
        cipher.iv + encrypted_bytes
    ).decode()

    return encrypted_data

# Decrypt message
def decrypt_message(encrypted_message, password):
    key = generate_key(password)

    encrypted_data = base64.b64decode(encrypted_message)

    iv = encrypted_data[:16]
    encrypted_bytes = encrypted_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(
        cipher.decrypt(encrypted_bytes),
        AES.block_size
    )

    return decrypted.decode()
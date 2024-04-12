import os
from cryptography.fernet import fernet
from bcrypt import hashpw, gensalt, checkpw
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode

def hash_password(password):
    return hashpw(password.encode(), gensalt())

def verify_password(stored_hash, password):
    return checkpw(password.encode(), stored_hash)

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

if __name__ == "__main__":
    password_hash = hash_password(password)
   
    salt = os.urandom(16)

    if verify_password(password_hash, password):
    key = derive_key(password, salt)

     original_message = "Sensitive data here"
     encrypted_message = encrypt_message(original_message, key)
     print(f"Encrypted: {encrypted_message}")

     decrypted_message = decrypt_message(encrypted_message, key)
     print(f"Decrypted: {decrypted_message}")

else:
    print("Invalid password, access denied.")



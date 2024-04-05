from cryptography.fernet import fernet

def generate_key():
    return fernet.generate_key()

def save_key(key, filename="secret.key"):
    with open(filename, "wb") as key_file:
        key_file.write(key)

def load_key(filename="secret.key")
    return open(filename, "rb").read()

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

if __name__ == "__main__":

key = generate_key()
save_key(key)

key = load_key()

original_message = "Sensitive data here"

encrypted_message = encrypted_message(original_message, key)
print(f"Encrypted: {encrypted message}")

decrypted_message = decrypted_message(encrypted_message, key)
print(f"Decrypted: {decrypted_message}")
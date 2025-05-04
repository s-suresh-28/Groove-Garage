from cryptography.fernet import Fernet

# Use your static Fernet key
SECRET_KEY = b"MSwQ2evOw4aT-JZ9XO23bRI-51IqCOTciZ1_3l4X5sQ="

cipher_suite = Fernet(SECRET_KEY)

def encrypt_message(message: str) -> bytes:
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    return cipher_suite.decrypt(encrypted_message).decode()

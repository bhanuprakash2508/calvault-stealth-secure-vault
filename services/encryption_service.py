import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv(
    "ENCRYPTION_KEY"
)

if KEY is None:

    raise ValueError(
        "ENCRYPTION_KEY is missing"
    )

CIPHER = Fernet(
    KEY.encode("utf-8")
)

# Text Encryption

def encrypt_data(data):

    return CIPHER.encrypt(
        data.encode()
    ).decode()


def decrypt_data(data):

    return CIPHER.decrypt(
        data.encode()
    ).decode()

# File Encryption

def encrypt_file(file_data):

    return CIPHER.encrypt(
        file_data
    )

def decrypt_file(file_data):

    return CIPHER.decrypt(
        file_data
    )
import os

# Encryption Decryption uses one single key to allow encryption and decryption
from cryptography.fernet import Fernet
from dotenv import load_dotenv  # This will allows us to load env files

# Loads .env file into scope
# load_dotenv("../.env")

KEY_FILE = "./data/fernet.key"


def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key


# SECRET_KEY = os.getenv('SECRET_KEY')
# assert SECRET_KEY

FERNET = Fernet(load_or_create_key())


# Function for easy encryption
# Pass in the data you want to encrypt and it will return the encrypted data
def encrypt(data):
    """
    Takes in uncrypted data and returns the encrypted version
    """
    return FERNET.encrypt(data.encode()).decode()


# Function for easy decryption
# Pass in encrypted data and it will decrypt it
def decrpyt(data):
    """
    Takes in encrypted data and returns decrypted data
    """
    return FERNET.decrypt(data).decode("utf-8")

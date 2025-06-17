import os

# Encryption Decryption uses one single key to allow encryption and decryption
from cryptography.fernet import Fernet
from dotenv import load_dotenv  # This will allows us to load env files

# Loads .env file into scope
load_dotenv("../.env")

SECRET_KEY = os.getenv('SECRET_KEY')
assert SECRET_KEY
FERNET = Fernet(SECRET_KEY)


# Function for easy encryption
# Pass in the data you want to encrypt and it will return the encrypted data
def encrypt(data):
    """
    Takes in uncrypted data and returns the encrypted version
    """
    return FERNET.encrypt(data.encode()).decode()


# Function for east decryption
# Pass in encrypted data and it will decrypt it
def decrpyt(data):
    """
    Takes in encrypted data and returns decrypted data
    """
    return FERNET.decrypt(data).decode("utf-8")

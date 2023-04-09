import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def make_key():
    # Generate RSA keys
    key = RSA.generate(2048)

    # Save private key to a file
    with open("payhere/security/private_key.pem", "wb") as f:
        f.write(key.export_key())

    # Export public key
    public_key = key.publickey().export_key()

    # Save public key to a file
    with open("payhere/security/public_key.pem", "wb") as f:
        f.write(public_key)

    # Import public key
    with open("payhere/security/public_key.pem", "rb") as f:
        recipient_key = RSA.import_key(f.read())

    # Encrypt password
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    password = "MyPassword123"
    encrypted_password = base64.b64encode(
        cipher_rsa.encrypt(password.encode())
    ).decode()

    # Import private key
    with open("payhere/security/private_key.pem", "rb") as f:
        private_key = RSA.import_key(f.read())

    # Decrypt password
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_password = cipher_rsa.decrypt(
        base64.b64decode(encrypted_password)
    ).decode()

    print("Original password:", password)
    print("Encrypted password:", encrypted_password)
    print("Decrypted password:", decrypted_password)


def encrypt_password(password: str) -> str:
    # Import public key
    with open("payhere/security/public_key.pem", "rb") as f:
        recipient_key = RSA.import_key(f.read())

    # Encrypt password
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_password = base64.b64encode(
        cipher_rsa.encrypt(password.encode())
    ).decode()

    return encrypted_password


def decrypt_password(encrypted_password: str) -> str:
    # Import private key
    with open("payhere/security/private_key.pem", "rb") as f:
        private_key = RSA.import_key(f.read())

    # Decrypt password
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_password = cipher_rsa.decrypt(
        base64.b64decode(encrypted_password)
    ).decode()

    return decrypted_password


if __name__ == "__main__":
    make_key()

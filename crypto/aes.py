import pyaes
import os


def aes_crypto(plaintext: str=None):
    """AES 加密"""
    # 16 byte block of plain text
    if not plaintext:
        plaintext = "Hello World!!!!!"
    plaintext_bytes = [ord(c) for c in plaintext]

    # key_value = os.urandom(32)
    key_value = b'\x18\x7f\xbb\xd7/\xcb\xe56~me<>\xefM>Zg\xc7\xd0\xaf|\xf3\xc7\xd5,D\tB&N\x9c'
    aes = pyaes.AES(key_value)

    print(plaintext_bytes)
    # Encrypt!
    ciphertext = aes.encrypt(plaintext_bytes)
    print(ciphertext)
    # Decrypt!
    decrypted = aes.decrypt(ciphertext)
    print(decrypted)

    result = ''
    for i in decrypted:
        result += chr(i)
    print(result)

if __name__ == '__main__':
    aes_crypto('123!@#qwe')
from Crypto.Util import number

# Funkcja szyfrująca RSA
def encrypt_rsa(plaintext, public_key):
    n, e = public_key
    ciphertext = [pow(byte, e, n) for byte in plaintext]
    return ciphertext

# Funkcja deszyfrująca RSA
def decrypt_rsa(ciphertext, private_key):
    n, d = private_key
    decrypted_data = []
    for byte in ciphertext:
        decrypted_byte = pow(byte, d, n)
        decrypted_data.append(decrypted_byte)
    return decrypted_data

cipherText = encrypt_rsa([156], (13261681, 10388423))
print(cipherText)
decrypted_data = decrypt_rsa(cipherText, (13261681, 159971))
print(decrypted_data)
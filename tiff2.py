import io
import imageio.v2 as imageio
import struct
import math
import random
import tifffile as tiff
from PIL import Image

# Funkcja szyfrująca RSA
def encrypt_rsa(plaintext, public_key):
    n, e = public_key
    ciphertext = [pow(byte, e, n) for byte in plaintext]
    return ciphertext

# Funkcja deszyfrująca RSA
def decrypt_rsa(ciphertext, private_key):
    n, d = private_key
    decrypted_data = [pow(byte, d, n) for byte in ciphertext]
    return decrypted_data

# Funkcja szyfrująca zawartość pliku TIFF
def encrypt_tiff(file_path, public_key):
    with Image.open(file_path) as img:
        data = list(img.tobytes())

    # Szyfrowanie masy bitowej pliku
    encrypted_data = encrypt_rsa(data, public_key)

    # Normalizacja zaszyfrowanych danych do zakresu 0-255
    normalized_data = [byte % 256 for byte in encrypted_data]

    # Konwersja zaszyfrowanych danych na obiekt bajtowy
    encrypted_bytes = bytes(normalized_data)

    # Odczytanie obrazu TIFF z odszyfrowanych danych
    img = Image.frombytes(img.mode, img.size, encrypted_bytes)
    encrypted_file_path = file_path.replace('.tiff', '_encrypted.tiff')
    img.save(encrypted_file_path)

    print("Plik TIFF został zaszyfrowany i zapisany jako:", encrypted_file_path)

# Funkcja deszyfrująca zawartość pliku TIFF
def decrypt_tiff(file_path, private_key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    # Deszyfrowanie zaszyfrowanych danych
    decrypted_data = decrypt_rsa(encrypted_data, private_key)

    # Normalizacja odszyfrowanych danych do zakresu 0-255
    normalized_data = [byte % 256 for byte in decrypted_data]

    # Konwersja odszyfrowanych danych na obiekt bajtowy
    decrypted_bytes = bytes(normalized_data)

    # Zapisanie odszyfrowanych danych jako plik TIFF
    decrypted_file_path = file_path.replace('_encrypted.tiff', '_decrypted.tiff')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_bytes)

    # Odczytanie zapisanego pliku TIFF za pomocą biblioteki PIL (Pillow)
    img = Image.open(decrypted_file_path)
    img.show()

    print("Plik TIFF został odszyfrowany i wyświetlony jako obraz.")

    return img


def generate_rsa_keys():
    # Funkcja generująca losową liczbę pierwszą
    def generate_prime_number():
        def is_prime(n):
            if n <= 1:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

        while True:
            prime_candidate = random.randint(2 ** 16, 2 ** 17)
            if is_prime(prime_candidate):
                return prime_candidate

    # Wygenerowanie dwóch różnych liczb pierwszych
    p = generate_prime_number()
    q = generate_prime_number()
    while p == q:
        q = generate_prime_number()

    n = p * q
    phi = (p - 1) * (q - 1)

    # Obliczenie liczby d za pomocą rozszerzonego algorytmu Euklidesa
    def extended_euclidean(a, b):
        if b == 0:
            return a, 1, 0
        d, x, y = extended_euclidean(b, a % b)
        return d, y, x - (a // b) * y

    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    _, _, d = extended_euclidean(e, phi)
    d %= phi
    if d < 0:
        d += phi

    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


# Przykładowe użycie funkcji
public_key, private_key = generate_rsa_keys()
encrypt_tiff('przyklad3.tiff', public_key)
decrypt_tiff('przyklad3_encrypted.tiff', private_key)

import math
import random
import numpy as np
import tifffile as tiff
from PIL import Image
from skimage import io

encrypt_data_tiff_black_white = []

def encrypt_rsa_black_white(plaintext, public_key):
    n, e = public_key
    ciphertext = [pow(byte, e, n) for byte in plaintext]
    return ciphertext

def decrypt_rsa_black_white(ciphertext, private_key):
    n, d = private_key
    decrypted_data = []
    for byte in ciphertext:
        decrypted_byte = pow(byte, d, n)
        decrypted_data.append(decrypted_byte)
    return decrypted_data

def encrypt_rsa_color(file_path, public_key):
    n, e = public_key
    image = Image.open(file_path).convert("RGB")
    image_array = np.array(image)
    height, width, _ = image_array.shape
    global encrypted_image_color_array
    encrypted_image_color_array = []

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = image_array[y, x]
            temp = [int(r), int(g), int(b)]
            ciphertext = [pow(byte, e, n) for byte in temp]
            row.append((ciphertext[0], ciphertext[1], ciphertext[2]))
            image_array[y, x] = ciphertext 
        encrypted_image_color_array.append(row)

    encrypted_image = Image.fromarray(image_array)
    
    encrypted_image.save("encrypted_image_color.tiff")

    return ciphertext

def decrypt_rsa_color(file_path, private_key):
    n, d = private_key
    decrypted_data = []
    image = Image.open(file_path).convert("RGB")
    image_array = np.array(image)
    height, width, _ = image_array.shape

    for y in range(height):
        for x in range(width):
            r, g, b = encrypted_image_color_array[y][x]
            temp = [int(r), int(g), int(b)]
            ciphertext = [pow(byte, d, n) for byte in temp]
            image_array[y, x] = ciphertext 

    decrypted_image = Image.fromarray(image_array)
    
    decrypted_image.save("decrypted_image_color.tiff")

    return decrypted_data

def encrypt_tiff(file_path, public_key):
    data = io.imread(file_path).astype(np.uint16)
    tiff.imwrite('black_white.tiff', np.array(data, dtype=np.uint8))
    encrypted_data = encrypt_rsa_black_white(data.flatten().tolist(), public_key)

    global encrypt_data_tiff_black_white 
    encrypt_data_tiff_black_white = encrypted_data.copy()

    encrypted_array = np.array(encrypted_data, dtype=np.uint16).reshape(data.shape)

    encrypted_file_path = file_path.replace('.tiff', '_encrypted.tiff')
    tiff.imwrite(encrypted_file_path, encrypted_array)

    print("Plik TIFF został zaszyfrowany i zapisany jako:", encrypted_file_path)

def decrypt_tiff(file_path, private_key):
    encrypted_data = tiff.imread(file_path).astype(np.uint16)

    decrypted_data = decrypt_rsa_black_white(encrypt_data_tiff_black_white, private_key)

    decrypted_array = np.array(decrypted_data, dtype=np.uint8).reshape(encrypted_data.shape)

    decrypted_file_path = file_path.replace('_encrypted.tiff', '_decrypted.tiff')
    tiff.imwrite(decrypted_file_path, decrypted_array)

    print("Plik TIFF został odszyfrowany i zapisany jako:", decrypted_file_path)

def generate_rsa_keys():
    def generate_prime_number():
        def is_prime(n):
            if n <= 1:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

        prime = random.randint(2**10, 2**12)
        while not is_prime(prime):
            prime = random.randint(2**10, 2**12)
        return prime
    
    p = generate_prime_number()
    q = generate_prime_number()
    while p == q:
        q = generate_prime_number()

    n = p * q
    phi = (p - 1) * (q - 1)

    def odwr_mod(a, n):
        a0, n0, p0, p1, q, r, t = 0, 0, 0, 1, 0, 0, 0
        p0 = 0
        p1 = 1
        a0 = a
        n0 = n
        q = n0 // a0
        r = n0 % a0

        while r > 0:
            t = p0 - q * p1
            if t >= 0:
                t = t % n
            else:
                t = n - ((-t) % n)
            p0 = p1
            p1 = t
            n0 = a0
            a0 = r
            q = n0 // a0
            r = n0 % a0

        return p1

    # Obliczenie liczby d za pomocą rozszerzonego algorytmu Euklidesa
    def extended_euclidean(a, b):
        if b == 0:
            return a, 1, 0
        d, x, y = extended_euclidean(b, a % b)
        return d, y, x - (a // b) * y

    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = odwr_mod(e, phi)

    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


public_key, private_key = generate_rsa_keys()
encrypt_rsa_color("przyklad3.tiff", public_key)
decrypt_rsa_color("encrypted_image_color.tiff", private_key)
encrypt_tiff('przyklad3.tiff', public_key)
decrypt_tiff('przyklad3_encrypted.tiff', private_key)
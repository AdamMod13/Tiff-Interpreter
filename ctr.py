from Crypto.Cipher import AES
from Crypto.Util import Counter
from PIL import Image

def encrypt_image(input_file, output_file, key):
    image = Image.open(input_file)
    width, height = image.size
    pixels = image.convert("RGB").tobytes()

    # Initialize AES cipher in CTR mode
    counter = Counter.new(128)
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)

    # Encrypt the image pixel data
    encrypted_pixels = cipher.encrypt(pixels)

    encrypted_image = Image.frombytes("RGB", (width, height), encrypted_pixels)

    encrypted_image.save(output_file)
    print("Image encrypted and saved successfully!")

input_file = "przyklad3.tiff"
output_file = "encrypted_ctr.tiff"
key = b"mysecretpassword"

# Encrypt the image
encrypt_image(input_file, output_file, key)
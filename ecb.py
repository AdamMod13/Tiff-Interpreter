from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import os

def encrypt_tiff_ecb(input_image_path, output_image_path, key):
    image = Image.open(input_image_path)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    image_data = image.tobytes()

    # Create an AES cipher object with ECB mode and the provided key
    cipher = AES.new(key, AES.MODE_ECB)

    # Pad the image data to be a multiple of the block size
    padded_data = pad(image_data, AES.block_size)

    # Encrypt the padded image data using ECB mode
    encrypted_data = cipher.encrypt(padded_data)

    encrypted_image = Image.frombytes(image.mode, image.size, encrypted_data)
    encrypted_image.save(output_image_path)


input_image_path = 'przyklad3.tiff'
output_image_path = 'encrypted_ecb.tiff'
key = b'Sixteen byte key'
encrypt_tiff_ecb(input_image_path, output_image_path, key)
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from PIL import Image


def generate_key_pair(key_size):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_image(image_path, public_key_data, output_path):
    # Load the image
    image = Image.open(image_path)
    width, height = image.size

    # Load the public key
    public_key = RSA.import_key(public_key_data)
    print(public_key)
    # Generate a symmetric encryption key
    symmetric_key = get_random_bytes(16)
    cipher_aes = AES.new(symmetric_key, AES.MODE_ECB)

    # Encrypt the image data with the symmetric key
    encrypted_data = b""
    chunk_size = 256
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            # Extract a chunk from the image
            chunk = image.crop((x, y, x + chunk_size, y + chunk_size))
            chunk_data = chunk.tobytes()

            # Encrypt the chunk with AES
            encrypted_chunk = cipher_aes.encrypt(chunk_data)
            encrypted_data += encrypted_chunk

    # Encrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(symmetric_key)

    # Create an encrypted image with the same size as the original image
    encrypted_image = Image.new(image.mode, (width, height))
    encrypted_image.frombytes(encrypted_data)

    # Save the encrypted image and encrypted key to files
    encrypted_image.save(output_path)
    with open('encrypted_key.bin', 'wb') as f:
        f.write(encrypted_key)


# Usage example
image_path = 'przyklad3.tiff'
output_path = 'encrypted_rsa.tiff'
key_size = 2048

# Generate RSA key pair
private_key, public_key = generate_key_pair(key_size)

# Save the private key to a file (optional)
with open('private_key.pem', 'wb') as f:
    f.write(private_key)

# Save the public key to a file
with open('public_key.pem', 'wb') as f:
    f.write(public_key)

# Encrypt the image using the generated public key
with open('public_key.pem', 'rb') as f:
    public_key_data = f.read()
    encrypt_image(image_path, public_key_data, output_path)

import colorsys

import numpy as np
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend


def chacha20_prng(key: bytes, length: int) -> bytes:
    """
    Generate pseudo-random bytes using ChaCha20 stream cipher.

    :param key: 32-byte key
    :param length: Number of random bytes to generate
    :return: Pseudo-random bytes of requested length
    """
    nonce = b'\x00' * 16 # Fixed nonce for deterministic PRNG output

    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    random_bytes = encryptor.update(b'\x00' * length)
    bit_string = ''.join(f'{byte:08b}' for byte in random_bytes)
    return bit_string

def load_img(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    rgb_array = np.array(image)
    return rgb_array

def get_luminance(pixel):
    # Luminance = 0.299*R + 0.587*G + 0.114*B
    return 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
def change_pixel_lightness(image, x, y, lightness_factor,n):
    """
    Change the lightness of a pixel at (x,y) by a factor (0.0 to 2.0).
    - 0.0 = black
    - 1.0 = original lightness
    - 2.0 = white
    """
    #r, g, b = image.getpixel((x, y))
    r = image[y][x][0]
    g = image[y][x][1]
    b = image[y][x][2]

    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    # Adjust lightness (clamp between 0 and 1)
    new_l = max(0, min(1, l * lightness_factor))

    # Convert back to RGB
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
    new_rgb = (int(new_r * 255), int(new_g * 255), int(new_b * 255))
    for i in range(n):
        image[y][x][0] = new_rgb[0]
        image[y][x][1] = new_rgb[1]
        image[y][x][2] = new_rgb[2]
    return image

def build_indices(n,bit_string,bits_size,imgX,imgY):
    a_indices = []
    b_indices = []

    for i in range(n):

        Ax = bit_string[i:i + bits_size]
        Ay = bit_string[i + bits_size:i + bits_size * 2]
        Bx = bit_string[i + bits_size * 3:i + bits_size * 4]
        By = bit_string[i + bits_size * 5:i + bits_size * 6]

        Ax = int(Ax, 2) % imgX
        Ay = int(Ay, 2) % imgY
        Bx = int(Bx, 2) % imgX
        By = int(By, 2) % imgY

        a_indices.append([Ax, Ay])
        b_indices.append([Bx, By])

    return a_indices,b_indices

def embed_patchwork(image_path,n,key):
    img = load_img(image_path)
    imgX = np.size(img, 1)
    imgY = np.size(img, 0)


    d=0.1
    bits_size = 10
    # Ax, Ay, Bx, By
    # 10 bits for each of coordinates(bits_size)
    # n pairs of those
    size = bits_size*n*4
    bit_string = chacha20_prng(key, size)

    #print(f"Random bit string: {bit_string}")
    a_indices, b_indices = build_indices(n,bit_string,bits_size,imgX,imgY)


    for a in a_indices:
        img = change_pixel_lightness(img,a[0],a[1],1+d,n)

    for b in b_indices:
        img = change_pixel_lightness(img,b[0],b[1],1-d,n)

    total_diff = 0
    for i in range(n):
        a_pixel = img[a_indices[i][1], a_indices[i][0]]  # (y, x) indexing
        b_pixel = img[b_indices[i][1], b_indices[i][0]]

        Ia = get_luminance(a_pixel)
        Ib = get_luminance(b_pixel)

        total_diff += (Ia - Ib)
    #S = 2*d*n+total_diff
    S = total_diff
    print(f"Embeded Patchwork statistic S = {S:.4f}")
    stamped_image = Image.fromarray(img)
    stamped_image.save('data/stamped_img.png', format='PNG', compress_level=0)
    return S

def decode_patchwork(image_path,n,key,S):
    img = load_img(image_path)
    imgX = np.size(img, 1)
    imgY = np.size(img, 0)
    d = 0.1
    bits_size = 10
    # Ax, Ay, Bx, By
    # 10 bits for each of coordinates(bits_size)
    # n pairs of those
    size = bits_size * n * 4
    bit_string = chacha20_prng(key, size)

    a_indices, b_indices = build_indices(n, bit_string, bits_size, imgX, imgY)

    total_diff = 0
    for i in range(n):
        a_pixel = img[a_indices[i][1], a_indices[i][0]]  # (y, x) indexing
        b_pixel = img[b_indices[i][1], b_indices[i][0]]

        Ia = get_luminance(a_pixel)
        Ib = get_luminance(b_pixel)

        total_diff += (Ia - Ib)
    Sn = total_diff
    print(f"Discovered Patchwork statistic S = {Sn:.4f}")
    if Sn != S:
        print("Watermarks dont match")
    else:
        print("Images match")

S=embed_patchwork("data/patchwork.png",10,b'secure_32_byte_key_for_chacha20!')
decode_patchwork("data/stamped_img.png",10,b'secure_32_byte_key_for_chacha20!',S)

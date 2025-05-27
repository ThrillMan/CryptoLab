# Least significant bit

from PIL import Image
import numpy as np


def load_img(file_path):
    image = Image.open(file_path)
    image = image.convert('RGB')
    rgb_array = np.array(image)
    return rgb_array


def string_to_binary(input_string):
    binary_string = ''.join(format(ord(char), '08b') for char in input_string)
    return binary_string


def binary_string_to_text(binary_string):
    n = 8
    chunks = [binary_string[i:i + n] for i in range(0, len(binary_string), n)]
    characters = [chr(int(chunk, 2)) for chunk in chunks]
    return ''.join(characters)

def encrypt_img(img,secret_password):
    secret_password = string_to_binary(secret_password)
    password_len = len(secret_password)
    imgX = np.size(img, 1)
    for i in range(0,password_len,3):
        index_x = i%imgX
        index_y = i // imgX
        if index_x<password_len:
            r = img[index_y][index_x][0]
            #print("r:", r)
            r = format(r, '08b')
            #print("r:", r)
            r = r[:-1] + secret_password[i]
            #print("r:",r)
            r = int(r, 2)
            #print("r:", r)
            img[index_y][index_x][0] = r
        if index_x+1<password_len:
            g = img[index_y][index_x][1]
            #print("g:", g)
            g = format(g, '08b')
            #print("g:", g)
            g = g[:-1] + secret_password[i+1]
            #print("g:", g)
            g = int(g, 2)
            #print("g:", g)
            img[index_y][index_x][1] = g
        if index_x+2<password_len:
            b = img[index_y][index_x][2]
            #print("b:", b)
            b = format(b, '08b')
            #print("b:", b)
            b = b[:-1] + secret_password[i+2]
            #print("b:", b)
            b = int(b, 2)
            #print("b:", b)
            img[index_y][index_x][2] = b
    return img
img = load_img('data/creeper.png')
img = encrypt_img(img,"Creeper")
secret_image = Image.fromarray(img)
secret_image.save('data/secret_img.png', format='PNG', compress_level=0)

def decrypt_img(img,password_len):
    secret_password = ""
    imgX = np.size(img, 1)
    for i in range(0, password_len, 3):
        index_x = i % imgX
        index_y = i // imgX
        if index_x < password_len:
            r = img[index_y][index_x][0]
            r = format(r, '08b')
            secret_password += r[-1]

        if index_x + 1 < password_len:
            g = img[index_y][index_x][1]
            g = format(g, '08b')
            secret_password += g[-1]

        if index_x + 2 < password_len:
            b = img[index_y][index_x][2]
            b = format(b, '08b')
            secret_password += b[-1]
    return binary_string_to_text(secret_password)

encrypted_img = load_img("data/secret_img.png")
secret_password = decrypt_img(encrypted_img,len("Creeper")*8)
print("Discovered password:",secret_password)

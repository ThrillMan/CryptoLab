from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
HEIGHT = 100
WIDTH = 100
def img_to_arr(file_path):
    img = Image.open(file_path).convert('1')
    img = np.array(img)
    og_img = img.astype(int)
    return og_img
def encrypt(img):
    first_part = [[0 for _ in range(WIDTH * 2)] for _ in range(HEIGHT)]
    second_part = [[0 for _ in range(WIDTH * 2)] for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            column = j * 2
            # White pixel
            if img[i][j]==1:
                if random.randint(0, 1)==0:
                    first_part[i][column]=0
                    first_part[i][column+1]=1

                    second_part[i][column] = 0
                    second_part[i][column + 1] = 1
                else:
                    first_part[i][column] = 1
                    first_part[i][column + 1] = 0

                    second_part[i][column] = 1
                    second_part[i][column + 1] = 0
            # Black pixel
            else:
                if random.randint(0, 1)==0:
                    first_part[i][column]=0
                    first_part[i][column+1]=1

                    second_part[i][column] = 1
                    second_part[i][column + 1] = 0
                else:
                    first_part[i][column] = 1
                    first_part[i][column + 1] = 0

                    second_part[i][column] = 0
                    second_part[i][column + 1] = 1
    # Saving both images:
    plt.imsave('data/first_part.bmp', np.array(first_part), cmap=cm.gray)
    plt.imsave('data/second_part.bmp', np.array(second_part), cmap=cm.gray)
def decrypt(img1,img2):
    decrypted_arr = [[0 for _ in range(WIDTH*2)] for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range((WIDTH*2)-1):
            # White pixel
            if img1[i][j+1]==1 and img2[i][j + 1]==1:
                decrypted_arr[i][j] = 0
                decrypted_arr[i][j + 1] = 1
            elif img1[i][j]==1 and img2[i][j]==1:
                decrypted_arr[i][j] = 1
                decrypted_arr[i][j+1] = 0
            # Black pixel
            else:
                decrypted_arr[i][j]=0
                decrypted_arr[i][j+1]=0

    plt.imsave('data/decrypted_img.bmp', np.array(decrypted_arr), cmap=cm.gray)

og_img = img_to_arr('data/3_inv.png')
encrypt(og_img)

og_img1 = img_to_arr("data/first_part.bmp")
og_img2 = img_to_arr("data/second_part.bmp")
decrypt(og_img1,og_img2)
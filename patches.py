import numpy as np
# import matplotlib.pyplot as plt
from PIL import Image
import cv2
import pdb
## make random patches
# https://github.com/marijavella/image-reconstructor-patches/blob/master/patch_reconstructor/recon_from_patches.py

GT = image = np.array(Image.open('Jungkook.png'))
# print(image)

stride = 128
patch_size = 128

# total 개수 세는 법을 모르겠어서,,,우선 야매,,
total =  (GT.shape[0]//(patch_size)) * (GT.shape[1]//(patch_size))
# print(total)
num_patches = 0
hr_patches = [[] for _ in range(total+1)] # img, position, patch_num

for i in range(0, GT.shape[0] - patch_size + 1, stride):
    for j in range(0, GT.shape[1] - patch_size + 1, stride):
        num_patches += 1
        hr_patches[num_patches].append(GT[i:i + patch_size, j:j + patch_size]) # patch image
        hr_patches[num_patches].append((i,j)) # position
        hr_patches[num_patches].append(num_patches) # patch number

# pdb.set_trace()

# if num_patches == total:
#     print(True)

# print(hr_patches)
# print(len(hr_patches))

for i in range(1, total+1):
    cv2.imwrite("patch_img{}.jpg".format(i), hr_patches[i][0])

im_h, im_w = GT.shape[0], GT.shape[1]

import random

img_num_pos = []
pos = []

for i in range(1, total+1):
    # print([hr_patches[i][0],hr_patches[i][2]])
    img_num_pos.append([hr_patches[i][0],hr_patches[i][2]])
    # img_num_pos.append()
    pos.append(hr_patches[i][1])
    # print(hr_patches[i][1:])
print(pos)
print(random.randint(len(pos)))

shuffle_pos = random.shuffle(pos)
print(shuffle_pos)
# print(pos_idx)
# print(len(imgs))
for j in range(0, total):
    img_num_pos[j].append(shuffle_pos[j])

print(len(img_num_pos)) # pos, patch_num, img, idx
print(img_num_pos)


# if len(GT.shape) == 2:
#     n_channels = 1
# else:
#     n_channels = GT.shape[2]

# patches = np.asarray(hr_patches)
# # print(patches)

# pdb.set_trace()

# def trans_format_RGB(data):
#     #tuple: Immutable, ensure that data is not lost
#     red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
#     pixels = tuple(zip(red, green, blue))
#     return pixels



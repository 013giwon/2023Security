import numpy as np
import random
from PIL import Image
import cv2
import pdb
## make random patches
# https://github.com/marijavella/image-reconstructor-patches/blob/master/patch_reconstructor/recon_from_patches.py
class Patches():
    def __init__(self):
        pass
    def patch_generation(self, GT, stride, patch_size ):
        #GT = image = np.array(Image.open('Jungkook.png'))
        GT = image = np.array(GT)
        stride = int(stride)
        patch_size = int(patch_size)

        # total 개수 세는 법을 모르겠어서,,,우선 야매,,
        total =  (GT.shape[0]//(patch_size)) * (GT.shape[1]//(patch_size))
        num_patches = 0
        hr_patches = [[] for _ in range(total+1)] # img, position, patch_num

        for i in range(0, GT.shape[0] - patch_size + 1, stride):
            for j in range(0, GT.shape[1] - patch_size + 1, stride):
                num_patches += 1
                hr_patches[num_patches].append(GT[i:i + patch_size, j:j + patch_size]) # patch image
                hr_patches[num_patches].append((i,j)) # position
                hr_patches[num_patches].append(num_patches) # patch number


        for i in range(1, total+1):
            cv2.imwrite("patch_img{}.jpg".format(i), hr_patches[i][0])

        im_h, im_w = GT.shape[0], GT.shape[1]

        
        patches_img =np.copy(GT)
        patches_img.fill(1)
        img_num_pos = []
        pos = []
        for i in range(1, total+1):
                pos.append(hr_patches[i][1])
                img_num_pos.append([hr_patches[i][0],hr_patches[i][2]])
                
        random.shuffle(pos)
        for i in range(0, total):

            patches_img[pos[i][0]:pos[i][0] +patch_size,pos[i][1]:pos[i][1] + patch_size,: ] = hr_patches[i+1][0]
        
        print(pos)

        for j in range(0, total):
            img_num_pos[j].append(pos[j])

        print(len(img_num_pos)) # pos, patch_num, img, idx
        print(img_num_pos)

        return patches_img #img_num_pos
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

        total =  (GT.shape[0]//(patch_size)) * (GT.shape[1]//(patch_size))
        num_patches = 0
        hr_patches = [[] for _ in range(total+1)] # img, position, patch_num

        for i in range(0, GT.shape[0] - patch_size + 1, stride):
            for j in range(0, GT.shape[1] - patch_size + 1, stride):
                num_patches += 1
                hr_patches[num_patches].append(GT[i:i + patch_size, j:j + patch_size]) # patch image
                hr_patches[num_patches].append((i,j)) # position
                hr_patches[num_patches].append(num_patches) # patch number


        # for i in range(1, total+1):
        #     cv2.imwrite("patch_img{}.jpg".format(i), hr_patches[i][0])

        patches_img =np.copy(GT)
        patches_img.fill(1)
        img_num_pos = []
        pos_original = []
        patch_num = []
        for i in range(1, total+1):
                pos_original.append(hr_patches[i][1])
                img_num_pos.append([hr_patches[i][2]])
                patch_num.append(hr_patches[i][2])
        
        indices = np.arange(len(pos_original))
        random.shuffle(indices)
        
        pos = []
        for i in range(len(pos_original)):
            pos.append(pos_original[indices[i]])

        for i in range(total):
            img_num_pos[i].append(pos[i])
            img_num_pos[i].append(indices[i])
            
        for i in range(0, total):
            patches_img[pos[i][0]:pos[i][0] +patch_size,pos[i][1]:pos[i][1] + patch_size,: ] = hr_patches[i+1][0]

 
        for j in range(0, total):
            img_num_pos[j].append(pos[j])
        # print(img_num_pos) # img_num_pos = [shuffled_idx, original_pos, original_idx, shuffled_pos]
        return patches_img, img_num_pos
 
    # shuff_key_list = [stride, patch_size, shuffled_dix]
    def patch_reconst(self, shuff_k, GT):             

        patch_size = shuff_k[1]
        stride = shuff_k[0]
        shuff_idx = shuff_k[2:]

        rec_pos = []
        patches_img =np.copy(GT)
        patches_img.fill(1)
        pos_original = []
        for i in range(0, GT.shape[0] - patch_size + 1, stride):
            for j in range(0, GT.shape[1] - patch_size + 1, stride):
                pos_original.append((i,j)) # position
        for i in range(len(shuff_idx)):
            rec_pos.append(pos_original[shuff_idx[i]])
        for i in range(len(shuff_idx)):
            patches_img[pos_original[i][0]:pos_original[i][0] + patch_size,pos_original[i][1]:pos_original[i][1] + patch_size,: ] = GT[rec_pos[i][0]:rec_pos[i][0] + patch_size,rec_pos[i][1]:rec_pos[i][1] + patch_size,: ]
        return patches_img
    # pdb.set_trace()

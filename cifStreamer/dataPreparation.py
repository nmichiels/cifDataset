"""
This module contains functions for data preprocessing
"""


import numpy as np
import math

def center_crop_pad(image, mask, maskChannel, blobIntensity, target_size, mode='symmetric'):
    """
    This function centers, crops and pads an image towards a target size.

    Args:
        image (np.array): Input image.
        mask (np.array): Input mask.
        maskChannel (int): What channel to use of mask image to calculate the center of the data.
        blobIntensity (int, optional): Blob id to use for centering.
        target_size (bool, optional): Target resolution of the output image.
        mode (str, optional, default=`symmteric`): Type of padding. Supports all modes of numpy.pad().
    
    Returns:
        np.array : a centered, cropped and padded image
    """

    # use first channel of mask to calculate center of mass
    # find the biggest blob
    center_of_mass = np.average(np.argwhere(mask[:,:,maskChannel] == blobIntensity), axis=0)

    center_x = int(np.floor(center_of_mass[0]))
    center_y = int(np.floor(center_of_mass[1]))

    half_size = int((target_size - 1) / 2)

    i_first = max(0, center_x-half_size)
    i_last = center_x+half_size+1
    j_first = max(0, center_y-half_size)
    j_last = center_y+half_size+1

    crop = image[i_first:i_last, j_first:j_last]
    pad_x = (int(np.floor((target_size - crop.shape[0]) / 2)), int(np.ceil((target_size - crop.shape[0]) / 2)))
    pad_y = (int(np.floor((target_size - crop.shape[1]) / 2)), int(np.ceil((target_size - crop.shape[1]) / 2)))
    pad_z = (0, 0)
    image = np.pad(crop, (pad_x, pad_y,pad_z), mode)
    crop = mask[i_first:i_last, j_first:j_last]
    mask = np.pad(crop, (pad_x, pad_y,pad_z), mode)
    return image, mask

   
def pad_or_crop(image, target_size, mode = 'symmetric', constant_values=(0)):
    """
    This function crops and pads an image towards a target size.

    Args:
        image (np.array): Input image.
        target_size (bool, optional): Target resolution of the output image.
        mode (str, optional, default=`symmteric`): Type of padding. Supports all modes of numpy.pad().

    Returns:
        np.array : a cropped and padded image
    """

    bigger = max(image.shape[0], image.shape[1], target_size)

    pad_x = float(bigger - image.shape[0])
    pad_y = float(bigger - image.shape[1])


    pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
    pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))
    pad_width_z = (0, 0)
    if (target_size > image.shape[0]) & (target_size > image.shape[1]):
        return np.pad(image, (pad_width_x, pad_width_y, pad_width_z), mode)
    else:
      
        if bigger > image.shape[1]:    
            temp_image = np.pad(image, ((0,0), pad_width_y,(0,0)), mode)

        else:
            if bigger > image.shape[0]:
                temp_image = np.pad(image, (pad_width_x,(0,0),(0,0)), mode)
            else:
                temp_image = image
        return temp_image[int((temp_image.shape[0] - target_size)/2):int((temp_image.shape[0] + target_size)/2),int((temp_image.shape[1] - target_size)/2):int((temp_image.shape[1] + target_size)/2)]

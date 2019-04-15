import numpy as np
import math

def center_crop_pad(image, mask, maskChannel, blobIntensity, target_size, mode='symmetric'):
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


# def pad_or_crop_zero(image, image_size):
#     bigger = max(image.shape[0], image.shape[1], image_size)

#     pad_x = float(bigger - image.shape[0])
#     pad_y = float(bigger - image.shape[1])

#     pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
#     pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))

#     if (image_size > image.shape[0]) & (image_size > image.shape[1]):
#         return np.pad(image, (pad_width_x, pad_width_y), 'constant', constant_values=(0))
#     else:
#         if bigger > image.shape[1]:
#             temp_image = np.pad(image, (pad_width_y), 'constant', constant_values=(0))
#         else:
#             if bigger > image.shape[0]:
#                 temp_image = np.pad(image, (pad_width_x), 'constant', constant_values=(0))
#             else:
#                 temp_image = image
#         return temp_image[int((temp_image.shape[0] - image_size)/2):int((temp_image.shape[0] + image_size)/2),int((temp_image.shape[1] - image_size)/2):int((temp_image.shape[1] + image_size)/2)]

   
def pad_or_crop(image, target_size, mode = 'symmetric', constant_values=(0)):
    bigger = max(image.shape[0], image.shape[1], target_size)

    pad_x = float(bigger - image.shape[0])
    pad_y = float(bigger - image.shape[1])


    pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
    pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))

    if (target_size > image.shape[0]) & (target_size > image.shape[1]):
        return np.pad(image, (pad_width_x, pad_width_y), mode)
    else:
        if bigger > image.shape[1]:
            temp_image = np.pad(image, (pad_width_y), mode)
        else:
            if bigger > image.shape[0]:
                temp_image = np.pad(image, (pad_width_x), mode)
            else:
                temp_image = image
        return temp_image[int((temp_image.shape[0] - target_size)/2):int((temp_image.shape[0] + target_size)/2),int((temp_image.shape[1] - target_size)/2):int((temp_image.shape[1] + target_size)/2)]



# def pad_or_crop(image, image_size):
#     bigger = max(image.shape[0], image.shape[1], image_size)

#     pad_x = float(bigger - image.shape[0])
#     pad_y = float(bigger - image.shape[1])

#     pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
#     pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))
#     # sample = image[int(image.shape[0]/2)-4:int(image.shape[0]/2)+4, :8]
#     sample = image[-10:,-10:]

#     std = np.std(sample)

#     mean = np.mean(sample)

#     def normal(vector, pad_width, iaxis, kwargs):
#         vector[:pad_width[0]] = np.random.normal(mean, std, vector[:pad_width[0]].shape)
#         vector[-pad_width[1]:] = np.random.normal(mean, std, vector[-pad_width[1]:].shape)
#         return vector



#     if (image_size > image.shape[0]) & (image_size > image.shape[1]):
#         return np.pad(image, (pad_width_x, pad_width_y), normal)
#     else:
#         if bigger > image.shape[1]:
#             temp_image = np.pad(image, (pad_width_y), normal)
#         else:
#             if bigger > image.shape[0]:
#                 temp_image = np.pad(image, (pad_width_x), normal)
#             else:
#                 temp_image = image
#         return temp_image[int((temp_image.shape[0] - image_size)/2):int((temp_image.shape[0] + image_size)/2),int((temp_image.shape[1] - image_size)/2):int((temp_image.shape[1] + image_size)/2)]

   


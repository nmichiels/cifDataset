import numpy as np
import math

def __pad_or_crop(image, image_size):
    bigger = max(image.shape[0], image.shape[1], image_size)

    pad_x = float(bigger - image.shape[0])
    pad_y = float(bigger - image.shape[1])

    pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
    pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))
    # sample = image[int(image.shape[0]/2)-4:int(image.shape[0]/2)+4, :8]
    sample = image[-10:,-10:]

    std = np.std(sample)

    mean = np.mean(sample)

    def normal(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = np.random.normal(mean, std, vector[:pad_width[0]].shape)
        vector[-pad_width[1]:] = np.random.normal(mean, std, vector[-pad_width[1]:].shape)
        return vector

    if (image_size > image.shape[0]) & (image_size > image.shape[1]):
        return np.pad(image, (pad_width_x, pad_width_y), normal)
    else:
        if bigger > image.shape[1]:
            temp_image = np.pad(image, (pad_width_y), normal)
        else:
            if bigger > image.shape[0]:
                temp_image = np.pad(image, (pad_width_x), normal)
            else:
                temp_image = image
        return temp_image[int((temp_image.shape[0] - image_size)/2):int((temp_image.shape[0] + image_size)/2),int((temp_image.shape[1] - image_size)/2):int((temp_image.shape[1] + image_size)/2)]

   


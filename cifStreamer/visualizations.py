import numpy as np
import scipy.misc
import cv2

from .dataPreparation import __pad_or_crop


def visualizeCIFDataset(dataset):
    dataset.reset()

    targetSize = 60
    imageCounter = 0
    while (not dataset.eod()):

        image, maskImage = dataset.nextImage()

        
        print ("Image " + repr(imageCounter), image.shape)
       
        for channel in range(image.shape[-1]):#range(0,1):#
            img = image[:,:,channel]
            img /= np.amax(img)
            mask = maskImage[:,:,channel]

            img = __pad_or_crop(img, targetSize)
            mask = __pad_or_crop(mask, targetSize)


            maxMask = np.amax(mask)
            if (maxMask != 0):
                mask /= maxMask
            # else:
                # break
            # scipy.misc.imsave('outfile.jpg', img)
            cv2.imwrite("cell_" + repr(imageCounter) + "_c_" + repr(channel) + ".jpg", img*255)
            cv2.imwrite("mask_" + repr(imageCounter) + "_c_" + repr(channel) + ".jpg", mask*255)
            cv2.imshow('image',img)
            cv2.imshow('mask',mask)
            chr = cv2.waitKey(20)
        
        imageCounter += 1
        if chr==27: # Esc key to exit
            break 

    cv2.destroyAllWindows()
import numpy as np
import cv2

import bioformats
import bioformats.formatreader

import javabridge
import javabridge.jutil

import scipy.misc

import h5py

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

   
class CIFDataSet(object):
    
    def __init__(self, cifFile):
        print('Initializing Dataset: ' + cifFile)
        javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')
        self._reader = bioformats.formatreader.get_image_reader("tmp", path=cifFile)

        self._nimages = javabridge.call(self._reader.metadata, "getImageCount", "()I")
        self._nchannels = javabridge.call(self._reader.metadata, "getChannelCount", "(I)I", 0)
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))

        self._current_image_ID = 0

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage(self):
        image = self._reader.read(series=self._current_image_ID)
        mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 2
        return image, mask

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 0

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages):
            return True
        else:
            return False


    def __del__(self):
        javabridge.kill_vm()


class HDF5DataSet(object):
    
    def __init__(self, hdf5File):
        print('Initializing Dataset: ' + hdf5File)
        self._hdf5 = h5py.File(hdf5File, "r")
        # images = len(rawDataset.keys())
        # print (repr(images))
        self._nimages = len(self._hdf5['raw'].keys())
        self._nchannels = 0
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))

        self._current_image_ID = 0

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage(self):
        imageGrp = self._hdf5["raw/cell_" + repr(self._current_image_ID )]
        image = imageGrp['image']
        mask = imageGrp['mask']
        # mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 1
        return image, mask

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 0

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages):
            return True
        else:
            return False


    def __del__(self):
        javabridge.kill_vm()

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




def convertToHDF5(inputFile, outputFile):
    try:
        print('Loading ' + inputFile)
        dataset = CIFDataSet(inputFile)
        dataset.reset()

        hdf5 = h5py.File(outputFile, "w")
        grp = hdf5.create_group("raw")
        print(repr(hdf5.name))  
        imageCounter = 0
        while (not dataset.eod()):
            image, mask = dataset.nextImage()

            imageGrp = grp.create_group("cell_" + repr(imageCounter))
            dsetImg = imageGrp.create_dataset("image", data=image)
            dsetMsk = imageGrp.create_dataset("mask", data=mask)
            imageCounter += 1

            if (imageCounter % 100 == 0):
               hdf5.flush()
               print("Image " + repr(imageCounter) + " written to file.")



    except RuntimeError as err:
        print("Converting CIF file to hdf5 failed.")
        print("RuntimeError error: {0}".format(err))
    except javabridge.jutil.JavaException as err:
        print("JavaBridge Error.")
        print("JavaException error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")

    # print(image)

dataset = CIFDataSet("../05-Aug-2015_A04-noBF.cif")
# dataset = HDF5DataSet("test.dhf5")
visualizeCIFDataset(dataset)
# convertToHDF5("../05-Aug-2015_A04-noBF.cif", "test.dhf5")
# if __name__ == "__main__":
#     __main__()

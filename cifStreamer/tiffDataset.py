import h5py
from .dataset import Dataset
from tifffile import imread
import numpy as np
from .dataPreparation import pad_or_crop
from PIL import Image


def read_pgm(  file ):
    pgmf = open(file, 'rb')
    """Return a raster of integers from a PGM as a list of lists."""
    version = pgmf.readline()
    line = pgmf.readline()
    while chr(line[0]) == '#':
        line = pgmf.readline()
    #assert pgmf.readline() == 'P2\n'
    (width, height) = [int(i) for i in line.split()]
    depth = int(pgmf.readline())

    assert depth <= 255
    

    image = np.zeros((height, width), dtype=int)
    #print("height", height)
    #print("width", width)
    raster = []

    for y in range(height):
        line = pgmf.readline().decode("ascii")
        line = line.split('\t')
        line = line[:-1]
        raster = raster + line
      
    raster = [int(i) for i in raster] 
    raster = np.asarray(raster, dtype=float).reshape((height, width))
        
    return raster


class TiffDataset(Dataset):
    
    def __init__(self, tiffPathPattern, maskPath = None, numChannels = 12):
        print('Initializing Tiff Dataset: ' + tiffPathPattern)
        Dataset.__init__(self)

        import glob

        self._pattern = tiffPathPattern
        self._maskpattern = maskPath
        


        # check amount of 
        #glob.glob('B57-15 + Nivo _%d*_Ch%d.ome.tif')

        # make regex for finding all files (first %d is the image id, second %d is the channel id)
        regex = self._pattern.replace("%d", "[0-9]*", 1)
        

        files = glob.glob(regex%(1))
        self._num_examples =  len(glob.glob(regex%(1)))
        
        for i in range(2,numChannels+1,1):
            print("Checking images of channel ", regex%i)
            if len(glob.glob(regex%(i))) != self._num_examples:
                raise IndexError("NUmber of input images for channel %d is not equal to channel 1."%i, len(glob.glob(regex%(i))), " != ", self._num_examples)
        self._num_channels = numChannels

        if self._maskpattern:
            # make regex for finding all mask files (first %d is the image id, second %d is the channel id)
            regex = self._maskpattern.replace("%d", "[0-9]*", 1)

            for i in range(1,numChannels+1,1):
                print("Checking images of channel ", regex%i)
                if len(glob.glob(regex%(i))) != self._num_examples:
                    raise IndexError("NUmber of input images for channel %d is not equal to channel 1."%i, len(glob.glob(regex%(i))), " != ", self._num_examples)

        
        #self._hdf5 = h5py.File(hdf5File, "r")
        ## images = len(rawDataset.keys())
        ## print (repr(images))

        #self._images = None
        #self._masks = None
        ## self._labels = None

        #self._num_examples = 0
        ## self._num_classes = 0
        #self._num_channels = 0

        #if "image" in self._hdf5.keys():
        #    self._images = self._hdf5["image"]
        #    self._num_examples = self._images.len()
        #    self._num_channels = self._images.shape[3]
        #if "mask" in self._hdf5.keys():
        #    self._masks = self._hdf5["mask"]
   
        print("Image Count: " + repr(self._num_examples))
        print("Channel Count: " + repr(self._num_channels))
        if not self._maskpattern:
            print("No mask info found.")

        self._index_in_epoch = 0

    def get(self, index, image_size = None):
        if (index >= self.num_examples):
            raise IndexError("datasetindex ouf of range")
        return self._images[index]

    def nextBatch_withmask(self, batch_size, image_size = None):
        raise NotImplementedError()
        """Return the next `batch_size` examples from this data set."""

    def nextImage_withmask(self):
        current_image_ID = self._index_in_epoch

        self._index_in_epoch += 1
        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            self._index_in_epoch = 0


        image = imread(self._pattern%(current_image_ID, 1))
        image = np.expand_dims(image, axis=2)
        for channel in range(1,self._num_channels):
            imageChannel = imread(self._pattern%(current_image_ID, channel+1))
            imageChannel = np.expand_dims(imageChannel, axis=2)
            image = np.append(image, imageChannel, axis=2)

        image = image.astype(np.float32)


        


        mask = read_pgm(self._maskpattern%(current_image_ID, 1))
        mask = np.expand_dims(mask, axis=2)
        for channel in range(1,self._num_channels):
            maskChannel = read_pgm(self._maskpattern%(current_image_ID, channel + 1))
            maskChannel = np.expand_dims(maskChannel, axis=2)
            mask = np.append(mask, maskChannel, axis=2)

        image = image.astype(np.float32)
        

        return image,mask




    def nextBatch(self, batch_size, image_size = None):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        end = self._index_in_epoch
        
        if end > self._num_examples:
            end = self._num_examples
            self._epochs_done += 1
            self._index_in_epoch = 0

        count = end-start
        # print("batch:", batch_size)
        # print("end: ", count)
        batch = np.ndarray(shape=(count, image_size,image_size, self.num_channels))

        for i in range(0,count):
            imageID = self._index_in_epoch-count+i

            image = imread(self._pattern%(imageID, 1))
            image = np.expand_dims(image, axis=2)
            for channel in range(1,self._num_channels):
                imageChannel = imread(self._pattern%(imageID, channel+1))
                imageChannel = np.expand_dims(imageChannel, axis=2)
                image = np.append(image, imageChannel, axis=2)

            image = image.astype(np.float32)
            batch[i] = pad_or_crop(image, image_size, 'symmetric')

        return batch



    def nextImage(self):
        current_image_ID = self._index_in_epoch

        self._index_in_epoch += 1
        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            self._index_in_epoch = 0


        image = imread(self._pattern%(current_image_ID, 1))
        image = np.expand_dims(image, axis=2)
        for channel in range(1,self._num_channels):
            imageChannel = imread(self._pattern%(current_image_ID, channel+1))
            imageChannel = np.expand_dims(imageChannel, axis=2)
            image = np.append(image, imageChannel, axis=2)

        image = image.astype(np.float32)
        return image



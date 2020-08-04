"""
A specialized dataset loader class for *.npy datasets, with support for labels.
"""

import numpy as np
from .dataset import Dataset

class NPDataset(Dataset):
    """A specialized class used to represent a numpy dataset. Overloaded from Dataset. In contains a dataset of images and labels"""

    def __init__(self, images, labels):
        Dataset.__init__(self)
        self._num_examples = images.shape[0]
        self._num_classes = labels.shape[1]
        self._num_channels = images.shape[3]
        self._images = images
        self._labels = labels
    

    @property
    def images(self):
        """Returns all the examples of this hdf5 dataset."""
        return self._images

    @property
    def labels(self):
        """Return all the labels of this entire numpy dataset."""
        return self._labels
          
    def nextBatch(self, batch_size, image_size = None):
        """Returns next `batch_size` of examples and masks from this numpy dataset."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        end = self._index_in_epoch
    
        if end > self._num_examples:
            end = self._num_examples
            self._epochs_done += 1
            self._index_in_epoch = 0

        return self._images[start:end], self._labels[start:end]
  
    def maxIntensityOfChannel(self, channel):
        """Returns the max intesity value of entire dataset for one specific channel."""
        if channel >= self.num_channels:
            raise Exception('Channel %d does not exist, num channels is %d'%(channel, self.num_channels))
        return np.max(self.images[:,:,:,channel])

    def minIntensityOfChannel(self, channel):
        """Returns the min intesity value of entire dataset for one specific channel."""
        if channel >= self.num_channels:
            raise Exception('Channel %d does not exist, num channels is %d'%(channel, self.num_channels))
        return np.min(self.images[:,:,:,channel])


    def nextImage(self):
        """Returns next example from this numpy dataset."""
        return self.nextBatch(1)   

    def get_batch(self, idx, batch_size, image_size):
        """Returns `batch_size` of examples and labels starting rom position `idx` from this numpy dataset."""
        start = idx*batch_size
        end = (idx+1)*batch_size
        if end > self._num_examples:
            end = self._num_examples
     
        return self._images[start:end], self._labels[start:end]

    def permutate(self):
        """Random shuffles then numpy dataset."""
        p = np.random.permutation(self._images.shape[0])
        self._images = self._images[p]
        self._labels = self._labels[p]
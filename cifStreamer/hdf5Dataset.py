"""
A specialized dataset loader class for *.hdf5 datasets.
"""

import h5py
from .dataset import Dataset

class HDF5Dataset(Dataset):
    """A class used to represent an HDF5 dataset. Overloaded from Dataset. In contains a dataset of images and masks"""
    
    def __init__(self, hdf5File):
        print('Initializing Dataset: ' + hdf5File)
        Dataset.__init__(self)

        self._images = None
        self._masks = None
        self._num_examples = 0
        self._num_channels = 0

        self._hdf5 = h5py.File(hdf5File, "r")
        if "image" in self._hdf5.keys():
            self._images = self._hdf5["image"]
            self._num_examples = self._images.len()
            self._num_channels = self._images.shape[3]
        if "mask" in self._hdf5.keys():
            self._masks = self._hdf5["mask"]
   
        print("Image Count: " + repr(self._num_examples))
        print("Channel Count: " + repr(self._num_channels))
        if not self._masks:
            print("No mask info found.")
     
        self._index_in_epoch = 0

    # get image at specific index
    def get(self, index, image_size = None):
        """Returns example  at specific `index` in this hdf5 dataset."""
        if (index >= self.num_examples):
            raise IndexError("datasetindex ouf of range")
        return self._images[index]


    def nextBatch_withmask(self, batch_size, image_size = None):
        """Returns next `batch_size` of examples and masks from this hdf5 dataset."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        end = self._index_in_epoch
        
        if end > self._num_examples:
            end = self._num_examples
            self._epochs_done += 1
            self._index_in_epoch = 0

        batch_mask = None
        if (self._masks):
            batch_mask = self._masks[start:end]


        return self._images[start:end], batch_mask


    def nextImage_withmask(self):
        """Return the next example and mask from this data set."""
        return self.nextBatch_withmask(1)


    def nextBatch(self, batch_size, image_size = None):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        end = self._index_in_epoch
        
        if end > self._num_examples:
            end = self._num_examples
            self._epochs_done += 1
            self._index_in_epoch = 0

        return self._images[start:end]

    def nextImage(self):
        """Returns next example of this hdf5 dataset."""
        return self.nextBatch(1)   

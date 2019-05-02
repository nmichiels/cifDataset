import h5py
from .dataset import Dataset

class HDF5Dataset(Dataset):
    
    def __init__(self, hdf5File):
        print('Initializing Dataset: ' + hdf5File)
        Dataset.__init__(self)


        self._hdf5 = h5py.File(hdf5File, "r")
        # images = len(rawDataset.keys())
        # print (repr(images))

        self._images = None
        self._masks = None
        # self._labels = None

        self._num_examples = 0
        # self._num_classes = 0
        self._num_channels = 0

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

    def get(self, index, image_size = None):
        if (index >= self.num_examples):
            raise IndexError("datasetindex ouf of range")
        return self._images[index]

    def nextBatch_withmask(self, batch_size, image_size = None):
        """Return the next `batch_size` examples from this data set."""
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


        return self._images[start:end], batch_mask#, self._labels[start:end]

    def nextImage_withmask(self):
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
        return self.nextBatch(1)   

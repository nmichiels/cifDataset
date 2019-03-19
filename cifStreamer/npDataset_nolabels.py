import numpy as np
from .dataset import Dataset

class NPDataset_nolabels(Dataset):

  def __init__(self, images):
    Dataset.__init__(self)

    self._num_examples = images.shape[0]
    self._num_channels = images.shape[3]


    self._images = images

    

  @property
  def images(self):
    return self._images

          
  def next_batch(self, batch_size, image_size = None):
    """Return the next `batch_size` examples from this data set."""
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    end = self._index_in_epoch
    
    if end > self._num_examples:
      end = self._num_examples
      self._epochs_done += 1
      self._index_in_epoch = 0

    return self._images[start:end]

  def get(self, index, image_size = None):
    if (index >= self.num_examples):
      raise IndexError("datasetindex ouf of range")

    return self._images[index]
      
  def nextImage(self):
    return self.next_batch(1)   

    

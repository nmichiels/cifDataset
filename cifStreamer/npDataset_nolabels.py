"""
A specialized dataset loader class for *.npy datasets, without support for labels.
"""

import numpy as np
from .dataset import Dataset

class NPDataset_nolabels(Dataset):  
  """A specialized dataset loader class for *.npy datasets, without support for labels."""
    
  def __init__(self, images):
    Dataset.__init__(self)
    self._num_examples = images.shape[0]
    self._num_channels = images.shape[3]
    self._images = images
    

  @property
  def images(self):
    """Return the entire array of images."""
    return self._images
    
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
    """Returns image at specific position `index` from this numpy dataset."""
    if (index >= self.num_examples):
      raise IndexError("datasetindex ouf of range")
    return self._images[index]
      

  def nextImage(self):
    """Returns next example from this numpy dataset."""
    return self.next_batch(1)   

    

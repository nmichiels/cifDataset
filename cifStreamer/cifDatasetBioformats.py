"""
A specialized dataset loader class for *.cif files, using the bioformats.
Warning: this dataset loader is a lot slower compared to cifDataset
"""


import bioformats
import bioformats.formatreader
import javabridge
import javabridge.jutil


class CIFDataset(object):
    """
    A specialized dataset loader class for *.cif files using BioFormats. Significantly slower compared to cifDataset.
    """

    def __init__(self, cifFile, overRuleChannelCount = None):
        """The constructor initializes the cif file and javabridge."""
        try:
            print('Initializing Dataset: ' + cifFile)
            javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')

            self._reader = bioformats.formatreader.get_image_reader("tmp", path=cifFile)

            jmd = javabridge.JWrapper(self._reader.rdr.getMetadataStore())
            print("ChannelName", jmd.getChannelName(1,0),jmd.getChannelName(1,1), jmd.getChannelName(1,2))
    
           

            self._nimages = int(jmd.getImageCount() / 2)
            self._nchannels = jmd.getChannelCount(0)
            print("Image Count: " + repr(self._nimages))
            print("Channel Count: " + repr(self._nchannels))

            if (overRuleChannelCount):
                print("BEWARE: overRuleChannelCount is not used in cifDatasetBioformats")
            self._current_image_ID = 0
         
        except javabridge.jutil.JavaException as err:
            print("JavaBridge Error.")
            print("JavaException error: {0}".format(err))

    def nextBatch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        print ("Next batch")
        # todo


    def nextImage_withmask(self):
        """Return the next example and mask from this data set."""
        image = self._reader.read(series=self._current_image_ID)
        mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 2
        return image, mask


    def nextImage(self):
        """Returns next example of this dataset."""
        image = self._reader.read(series=self._current_image_ID)
        self._current_image_ID += 2
        return image


    # set dataset back to first image
    def reset(self):
        """This function reset the dataset and will restart at the first image."""
        super().reset()
        self._current_image_ID = 0

    # check if end of dataset
    def eod(self):
        """Returns if the end of the dataset is reached, i.e. iterated over all the images of the dataset."""
        if (self._current_image_ID >= self._nimages*2):
            return True
        else:
            return False

    def numberOfImages(self):
        """Returns the number of images in the dataset."""
        return self._nimages

    def numberOfChannels(self):
        """Returns the number of channels in the dataset."""
        return self._nchannels

    def __del__(self):
        javabridge.kill_vm()
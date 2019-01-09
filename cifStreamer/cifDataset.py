import builtins
# from cifDataset.cifStreamer.FlowSightParser import FlowSightParser
from cifDataset.cifStreamer.FlowSightParserC import FlowSightParser

class CIFDataset(object):
    
    def __init__(self, cifFile):
      
        print('Initializing Dataset: ' + cifFile)
        

        self._flowSightParser = FlowSightParser()
        if not self._flowSightParser.loadFile(cifFile):
            print("ERROR (CIFDataset): Could not open file \"", cifFile, "\"")
            self._nimages = 0
            self._nchannels = 0
            return

        self._flowSightParser.loadMetaData(verbose=False)

        self._nimages = int(self._flowSightParser._numCells / 2)
        self._nchannels = self._flowSightParser._channelCount
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))

        self._current_image_ID = 1
        

      

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage(self):
        if (self._current_image_ID >self._nimages*2):
            return None, None
        image = self._flowSightParser.openIFDData(self._current_image_ID , verbose=False)
        mask = self._flowSightParser.openIFDData(self._current_image_ID+1 , verbose=False)
        self._current_image_ID += 2
        return image, mask

    def nextImage_nomask(self):
        if (self._current_image_ID >self._nimages*2):
            return None
        image = self._flowSightParser.openIFDData(self._current_image_ID , verbose=False)
        # mask = self._flowSightParser.openIFDData(self._current_image_ID+1 , verbose=False)
        self._current_image_ID += 2
        return image

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 1

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages*2+1):
            return True
        else:
            return False

    def numberOfImages(self):
        return self._nimages

    def numberOfChannels(self):
        return self._nchannels

    def __del__(self):
        pass
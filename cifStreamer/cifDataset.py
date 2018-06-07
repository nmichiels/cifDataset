import bioformats
import bioformats.formatreader
import javabridge
import javabridge.jutil

class CIFDataset(object):
    
    def __init__(self, cifFile):
        try:
            print('Initializing Dataset: ' + cifFile)
            javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')
            self._reader = bioformats.formatreader.get_image_reader("tmp", path=cifFile)

            self._nimages = javabridge.call(self._reader.metadata, "getImageCount", "()I")
            self._nchannels = javabridge.call(self._reader.metadata, "getChannelCount", "(I)I", 0)
            print("Image Count: " + repr(self._nimages))
            print("Channel Count: " + repr(self._nchannels))

            self._current_image_ID = 0
        except javabridge.jutil.JavaException as err:
            print("JavaBridge Error.")
            print("JavaException error: {0}".format(err))

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

    def numberOfImages(self):
        return self._nimages

    def numberOfChannels(self):
        return self._nchannels

    def __del__(self):
        javabridge.kill_vm()
import numpy as np
import cv2

import bioformats
import bioformats.formatreader

import javabridge
import javabridge.jutil

def __initFile(inputFile):
    try:
        print('Initializing ' + inputFile)
        dataset = CIFDataSet()
        dataset.loadingCells(inputFile)

    except RuntimeError as err:
        print("Streaming CIF file failed.")
        print("RuntimeError error: {0}".format(err))
    # finally:
        # fh.closed

    # print(image)

   
class CIFDataSet(object):
    
    def __init__(self):
        print('Initializing')
        javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')
        

    def loadingCells(self, cifFile):
        print('Initializing Dataset: ' + cifFile)
        self._reader = bioformats.formatreader.get_image_reader("tmp", path=cifFile)

        print('Loading Cell Data')
        image_count = javabridge.call(self._reader.metadata, "getImageCount", "()I")
        print("Image Count: " + repr(image_count))



    def __del__(self):
        javabridge.kill_vm()

__initFile("../example.cif")
# if __name__ == "__main__":
#     __main__()

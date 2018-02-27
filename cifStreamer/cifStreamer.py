import numpy as np
import cv2

import bioformats
import bioformats.formatreader

import javabridge
import javabridge.jutil

import scipy.misc

def __initFile(inputFile):
    try:
        print('Initializing ' + inputFile)
        dataset = CIFDataSet()
        dataset.loadingCells(inputFile)

    except RuntimeError as err:
        print("Streaming CIF file failed.")
        print("RuntimeError error: {0}".format(err))
    except javabridge.jutil.JavaException as err:
        print("JavaBridge Error.")
        print("JavaException error: {0}".format(err))
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
        channel_count = javabridge.call(self._reader.metadata, "getChannelCount", "(I)I", 0)
        print("Image Count: " + repr(image_count))
        print("Channel Count: " + repr(channel_count))

        chr = 0
        for imageID in range(0,image_count,2):
            print("Image " + repr(imageID))
            image = self._reader.read(series=imageID)
            maskImage = self._reader.read(series=imageID+1)

            for channel in range(0,1):#range(image.shape[-1]):
                img = image[:,:,channel]
                img /= np.amax(img)
                mask = maskImage[:,:,channel]
                maxMask = np.amax(mask)
                if (maxMask != 0):
                    mask /= maxMask
                # scipy.misc.imsave('outfile.jpg', img)
 
                cv2.imshow('image',img)
                cv2.imshow('mask',mask)
                chr = cv2.waitKey(500)
            
           
            if chr==27: # Esc key to exit
                break 

                

        
        cv2.destroyAllWindows()

    def __del__(self):
        javabridge.kill_vm()

__initFile("../example.cif")
# if __name__ == "__main__":
#     __main__()

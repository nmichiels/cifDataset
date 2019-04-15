# converting hdf5 of cif dataset to numpy data

import sys
import numpy as np
from cifStreamer.hdf5Dataset import HDF5Dataset
# from cifStreamer.cifDataset import CIFDataset
from cifStreamer.dataPreparation import pad_or_crop
# from cifStreamer.dataPreparation import pad_or_crop_zero

if (len(sys.argv) < 4 or len(sys.argv) > 7):
    print("Wrong parameters. Use \"", sys.argv[0], "inputFile outputNumpy targetSize [outputMask] [numImages] [channels]\"")
    sys.exit(1)

inputFile = sys.argv[1]
outputFile = sys.argv[2]
img_size = int(sys.argv[3])



channelsString = None
if (len(sys.argv) == 7):
    channelsString = sys.argv[6]

if (not outputFile):
    print("No output file specified")
if inputFile.endswith('.cif'):
    dataset = CIFDataset(sys.argv[1])
elif inputFile.endswith('.hdf5'):
    dataset = HDF5Dataset(sys.argv[1])
else:
    print("Not a valid input file")
    sys.exit(1)



channels = np.arange(dataset.num_channels)
if (channelsString):
    channels = channelsString.split(",")
    channels = np.asarray(channels, dtype=int, order=None)

numChannels = channels.shape[0]
print("channels: ", channels)
print("numChannels:",numChannels)


def next_batch(dataset, image_size, batch_size, channels):
    
    numChannels = channels.shape[0]
    batch = np.ndarray(shape=(batch_size, image_size,image_size, numChannels))
    batch_mask = np.ndarray(shape=(batch_size, image_size,image_size, numChannels))

    for i in range(0,batch_size):
        image, mask = dataset.nextImage_withmask()

        # if (i % 100 == 0):
        #     print(i)

        for idx, channel in enumerate(channels):
            img = image[:,:,channel]
            msk = mask[:,:,channel]

            batch[i][:,:,idx] = pad_or_crop(img, image_size, 'symmetric')# pad_or_crop(img, image_size, 'constant', constant_values=(0))
            batch_mask[i][:,:,idx] = pad_or_crop(msk, image_size, 'symmetric')# pad_or_crop(img, image_size, 'constant', constant_values=(0))
            # print (imgCropped)
    return batch, batch_mask


outputFileMask = None
if (len(sys.argv) > 4):
    outputFileMask = sys.argv[4]


batchSize = dataset.num_examples
if (len(sys.argv) > 5):
    batchSize = min(int(sys.argv[5]),batchSize)
    print("NumImages:", batchSize)




# data, masks = next_batch(dataset, img_size, batchSize, channels)
data, masks = dataset.nextBatch_withmask(batchSize)
data = data[:,:,:,channels]
np.save(outputFile, data)
if outputFileMask is not None:
    np.save(outputFileMask, masks)
print("Saved numpy array with shape", repr(data.shape))
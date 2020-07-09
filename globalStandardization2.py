import numpy as np
import sys



def globalStandardization(input1, input2, output1, output2):
    """
    This function applies global standardization on the merged input1 and input2 dataset. The result is splitted again and stored into output1 and output2.
    This is usefull when you have seperated training classes per file and you want to merge them temporarely to apply standardization.

    Args:
        input1 (str): Numpy dataset 1 [num_images, image_size, image_size, num_channels]
        input2 (str): Numpy dataset 2 [num_images, image_size, image_size, num_channels]
        output1 (str): Output global standarized dataset 1 [num_images, image_size, image_size, num_channels]
        output2 (str): Output global standarized dataset 2 [num_images, image_size, image_size, num_channels]
    """

    data1 = np.load(input1)
    data2 = np.load(input2)
    data = np.concatenate((data1, data2), axis=0)

    means = data.mean(axis=(0,1,2), dtype='float64')
    stds = data.std(axis=(0,1,2), dtype='float64')

    for i, img in enumerate(data1):
        for c in range(data1.shape[-1]):
            data1[i,:,:,c] = (img[:,:,c] - means[c]) / stds[c]
    np.save(output1, data1)

    for i, img in enumerate(data2):
        for c in range(data2.shape[-1]):
            data2[i,:,:,c] = (img[:,:,c] - means[c]) / stds[c]
    np.save(output2, data2)

   

def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 3 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python inputClass1.npy inputClass2.npy outputClass1.npy outputClass2.npy")
    else:
        globalStandardization(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()



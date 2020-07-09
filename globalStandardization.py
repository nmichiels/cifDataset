import numpy as np
import sys



def globalStandardization(input, output):
    """
    This function applies global standardization to the input dataset and stores to the output dataset.
    Args:
        input (str): Numpy file containing dataset with shape [num_images, image_size, image_size, num_channels]
        output (str): Output numpy file containing global standarized dataset with shape [num_images, image_size, image_size, num_channels]
    """

    data = np.load(input)
    means = data.mean(axis=(0,1,2), dtype='float64')
    stds = data.std(axis=(0,1,2), dtype='float64')

    for i, img in enumerate(data):
        for c in range(data.shape[-1]):
            data[i,:,:,c] = (img[:,:,c] - means[c]) / stds[c]
    np.save(output, data)
   

def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 3 or len(sys.argv) > 3):
        print("Wrong number of input arguments. Usage: python input.npy output.npy")
    else:
        globalStandardization(sys.argv[1],sys.argv[2])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()



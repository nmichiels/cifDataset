import numpy as np
import sys



def localStandardization(input, output):
    """
    This function applies local standardization per image in the input dataset. The standardized dataset is saved to output.
    Args:
        input (str): Numpy file containing dataset with shape [num_images, image_size, image_size, num_channels]
        output (str): Output numpy file containing locally standarized dataset with shape [num_images, image_size, image_size, num_channels]
    """

    data = np.load(input)
    # Local Standardization
    # calculate per-channel means and standard deviations
    for i, img in enumerate(data):
        means = img.mean(axis=(0,1), dtype='float64')
        stds = img.std(axis=(0,1), dtype='float64')
        # per-channel standardization of pixels
        data[i,:,:,:] = (img - means) / stds

    np.save(output, data)
   

def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 3 or len(sys.argv) > 3):
        print("Wrong number of input arguments. Usage: python input.npy output.npy")
    else:
        localStandardization(sys.argv[1],sys.argv[2])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()



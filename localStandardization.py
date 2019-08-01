import numpy as np
import sys



def localStandardization(input, output):
    data = np.load(input)
    # Local Standardization
    # calculate per-channel means and standard deviations
    for i, img in enumerate(data):
        # print("img:" , img.shape)
        means = img.mean(axis=(0,1), dtype='float64')
        stds = img.std(axis=(0,1), dtype='float64')
        # print('Means: %s, Stds: %s' % (means, stds))
        # per-channel standardization of pixels
        data[i,:,:,:] = (img - means) / stds
        # confirm it had the desired effect
        # means = img.mean(axis=(0,1), dtype='float64')
        # stds = img.std(axis=(0,1), dtype='float64')
        # print('Means: %s, Stds: %s' % (means, stds))
    np.save(output, data)
   

def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 3 or len(sys.argv) > 3):
        print("Wrong number of input arguments. Usage: python input.npy lsoutput.npy")
    else:
        localStandardization(sys.argv[1],sys.argv[2])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()



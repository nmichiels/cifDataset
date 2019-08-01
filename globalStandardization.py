import numpy as np
import sys



def globalStandardization(input, output):
    data = np.load(input)
    # Local Standardization
    # calculate per-channel means and standard deviations for all datasamples

    means = data.mean(axis=(0,1,2), dtype='float64')

    print(means.shape)
    stds = data.std(axis=(0,1,2), dtype='float64')
    print(means)
    for i, img in enumerate(data):
        for c in range(data.shape[-1]):
            # print(c)
            data[i,:,:,c] = (img[:,:,c] - means[c]) / stds[c]
    # for i, img in enumerate(data):
    #     data[i,:,:,:] = (img - means) / stds
    print(data)
    np.save(output, data)
   

def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 3 or len(sys.argv) > 3):
        print("Wrong number of input arguments. Usage: python input.npy lsoutput.npy")
    else:
        globalStandardization(sys.argv[1],sys.argv[2])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()



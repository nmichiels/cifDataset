import numpy as np
import sys



def globalStandardization(input1, input2, output1, output2):
    data1 = np.load(input1)
    data2 = np.load(input2)

    data = np.concatenate((data1, data2), axis=0)
    # Local Standardization
    # calculate per-channel means and standard deviations for all datasamples
    print(data.dtype)
    means = data.mean(axis=(0,1,2), dtype='float64')
    stds = data.std(axis=(0,1,2), dtype='float64')
    print(means)
    for i, img in enumerate(data1):
        for c in range(data1.shape[-1]):
            # print(c)cd -
            data1[i,:,:,c] = (img[:,:,c] - means[c]) / stds[c]
    np.save(output1, data1)

    for i, img in enumerate(data2):
        for c in range(data2.shape[-1]):
            # print(c)
            data2[i,:,:,c] = (img[:,:,c] - means[c]) / stds[c]
    np.save(output2, data2)

    # for i, img in enumerate(data1):
    #     data1[i,:,:,:] = (img - means) / stds
    # np.save(output1, data1)

    # for i, img in enumerate(data2):
    #     data2[i,:,:,:] = (img - means) / stds
    # np.save(output2, data2)
   

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



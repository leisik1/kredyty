import numpy as np
import scipy
import scipy.linalg

example1 = [0,0,1,2,3,4,4,3,2,1,0,0,0,0,0,0,0]
example2 = [0,0,0,1,1,2,2,3,3,3,3,2,0,0,0,0,0]

const = 0.1
example1 = [i+const for i in example1]
example2 = [i+const for i in example2]

def KLD(data0,data1):
    data1 = data1 / scipy.linalg.norm(data1,ord=1)
    data0 = data0 / scipy.linalg.norm(data0,ord=1)
    kld_data = []
    for i in range(len(example1)):
        kld_data.append(data1[i]*np.log(data1[i]/data0[i]))
    return sum(kld_data)

print(KLD(example1,example2))


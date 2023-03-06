import numpy as np
import scipy
import matplotlib.pyplot as plt
import csv


def printsci(str):
    print("{:e}".format(str))

with open(".\kredyty\credit_sample.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = []
    for i in range(4000):
        data_read.append(next(reader))
    # data_read = [row for row in reader]

Vars = [i[2:-1] for i in data_read]
Vars = [[float(lis[i]) for lis in Vars[1:] if not lis[i]=='NA'] for i in range(39)]

###
###
###

print(max(Vars[0]))

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zero(len(d))
    return data[s<m]

def showhistogram(var,nbins,rejectvalue):
    varrejected = reject_outliers(np.array(var), rejectvalue)
    hist = np.histogram(varrejected, nbins)
    print(hist[1])
    
    fig1, ax = plt.subplots()
    ax.bar(hist[1][:-1], hist[0], width=np.diff(hist[1]), edgecolor="black", align="edge")
    plt.show()
    plt.close(fig1)    

varcent1 = [i for i in Vars[0] if i <6.768e11]
showhistogram(Vars[4], 100, 2)
printsci(np.percentile(Vars[0],98))

print(Vars[0][:10])
printsci()

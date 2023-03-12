import numpy as np
import scipy
import scipy.linalg
import matplotlib.pyplot as plt
import csv
import statistics

with open(".\sorted_data.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    jebutna_lista = []
    for i in range(100):#148900
        jebutna_lista.append(next(reader))

companies = {}
id_now = "0"

for line in jebutna_lista:
    if id_now != line[0]:
        id_now = line[0]
        companies[id_now] = [line[1:]]
    else:
        companies[id_now].append(line[1:])

print(companies)

companies_def = {k:v for (k,v) in companies.items() if True in [bool(int(val[-1])) for val in companies[k]]}
companies_nondef = {k:v for (k,v) in companies.items() if not (True in [bool(int(val[-1])) for val in companies[k]])}

print(companies_def)

def W_i(data):
    res = []
    for i in range(len(data)):
        if data[i][4] != 'NA':
            res.append(float(data[i][4]))
    return np.average(res)


distrib_wyjebane_firmy = [W_i(val) for val in companies_def.values()]
distrib_git_firmy = [W_i(val) for val in companies_nondef.values()]

perc10_1=np.percentile(distrib_wyjebane_firmy,10)
perc90_1=np.percentile(distrib_wyjebane_firmy,90)

perc10_0=np.percentile(distrib_git_firmy,10)
perc90_0=np.percentile(distrib_git_firmy,90)

distrib_wyjebane_firmy_truncated = [i for i in distrib_wyjebane_firmy if (i > perc10_1 and i < perc90_1)]
distrib_git_firmy_truncated = [i for i in distrib_git_firmy if (i > perc10_0 and i < perc90_0)]

print(distrib_wyjebane_firmy)
print(distrib_wyjebane_firmy_truncated)

print(distrib_git_firmy)
print(distrib_git_firmy_truncated)

### Wskaźnik rozbieżności Hirohito-Himmlera

def KLD(data0,data1):
    data1 = data1 / scipy.linalg.norm(data1,ord=1)
    data0 = data0 / scipy.linalg.norm(data0,ord=1)
    kld_data = []
    for i in range(len(data0)):
        kld_data.append(data1[i]*np.log(data1[i]/data0[i]))
    return sum(kld_data)
import numpy as np
import scipy
import scipy.linalg
import matplotlib.pyplot as plt
import csv
import math
import statistics

with open(".\sorted_data.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    jebutna_lista = []
    for i in range(100000):#148900
        jebutna_lista.append(next(reader))

companies = {}
id_now = "0"

for line in jebutna_lista:
    if id_now != line[0]:
        id_now = line[0]
        companies[id_now] = [line[1:]]
    else:
        companies[id_now].append(line[1:])

# print(companies)

companies_def = {k:v for (k,v) in companies.items() if True in [bool(int(val[-1])) for val in companies[k]]}
companies_nondef = {k:v for (k,v) in companies.items() if not (True in [bool(int(val[-1])) for val in companies[k]])}

# print(companies_def)

# def W_i0(data,no):
#     res = []
#     for i in range(len(data)):
#         try:
#             # if (data[i][no] != 'NA' and data[i][2] != 'NA' and float(data[i][2]) != 0):
#             res.append(float(data[i][no]))
#         except:
#             pass
#     return np.average(res)

def W_i(data,no):
    res = []
    for i in range(len(data)):
        try:
            # if (data[i][no] != 'NA' and data[i][2] != 'NA' and float(data[i][2]) != 0):
            # x= float(data[i][no])/float(data[i][2])
            # if not math.isnan(x):
            #     res.append(x)


            # res.append((float(data[i][7])+float(data[i][8])+float(data[i][29]))/float(data[i][2]))
            res.append(float(data[i][no])/float(data[i][2]))
        except:
            # print(data[i][no])
            pass
    # if  math.isnan(np.average(res)):
    #     print(res)
    return np.average(res)


distrib_wyjebane_firmy = [W_i(val,5) for val in companies_def.values()]
distrib_git_firmy = [W_i(val,5) for val in companies_nondef.values()]
distrib_wyjebane_firmy = [i for i in distrib_wyjebane_firmy if i < 0 or i>0]
distrib_git_firmy = [i for i in distrib_git_firmy if i < 0 or i>0]

# print(distrib_git_firmy)

perc10_1=np.percentile(distrib_wyjebane_firmy,10)
perc90_1=np.percentile(distrib_wyjebane_firmy,90)

perc10_0=np.percentile(distrib_git_firmy,7)
perc90_0=np.percentile(distrib_git_firmy,93)

distrib_wyjebane_firmy_truncated = [i for i in distrib_wyjebane_firmy if (i >= perc10_1 and i <= perc90_1)]
distrib_git_firmy_truncated = [i for i in distrib_git_firmy if (i >= perc10_0 and i <= perc90_0)]

# print(distrib_git_firmy_truncated)

# print(distrib_wyjebane_firmy)
# print(distrib_wyjebane_firmy_truncated)

# print(distrib_git_firmy)
# print(distrib_git_firmy_truncated)

###
### Histogram / rozkład prawdopod.
###




hist1,bins1 = np.histogram(distrib_wyjebane_firmy_truncated, bins=20)
# print(hist1)

# Normalizacja:
hist1 = hist1 / sum(hist1)
# print(hist1)

hist0,bins0 = np.histogram(distrib_git_firmy, bins=bins1)
# print(hist0)

# Normalizacja:
hist0 = hist0 / sum(hist0)
# print(hist0)



# fig1, ax = plt.subplots()
# ax.bar(bins1[:-1], hist1, width=np.diff(bins1), color="red", align="edge",alpha=0.8)
# ax.bar(bins0[:-1], hist0, width=np.diff(bins0), color="green", align="edge",alpha=0.8)
# plt.show()
# plt.close()


###
### Wskaźnik rozbieżności Hirohito-Himmlera
###

def KLD(data0,data1):
    data1 = data1 / scipy.linalg.norm(data1,ord=1)
    data0 = data0 / scipy.linalg.norm(data0,ord=1)
    kld_data = []
    for i in range(len(data0)):
        kld_data.append(data1[i]*np.log(data1[i]/data0[i]))
    return sum(kld_data)

print(KLD(hist0,hist1))

####

def data_to_KLD(datadef,datandef,no):
    distrib_wyjebane_firmy = [W_i(val,no) for val in datadef.values()]
    distrib_git_firmy = [W_i(val,no) for val in datandef.values()]
    distrib_wyjebane_firmy = [i for i in distrib_wyjebane_firmy if i < 0 or i>0]
    distrib_git_firmy = [i for i in distrib_git_firmy if i < 0 or i>0]
    perc10_1=np.percentile(distrib_wyjebane_firmy,10)
    perc90_1=np.percentile(distrib_wyjebane_firmy,90)
    distrib_wyjebane_firmy_truncated = [i for i in distrib_wyjebane_firmy if (i >= perc10_1 and i <= perc90_1)]

    hist1,bins1 = np.histogram(distrib_wyjebane_firmy_truncated, bins=20)
    # Normalizacja:
    hist1 = hist1 / sum(hist1)

    hist0,bins0 = np.histogram(distrib_git_firmy, bins=bins1)
    # Normalizacja:
    hist0 = hist0 / sum(hist0)
    return KLD(hist0,hist1)

kld_val = []
for i in range(3,40):
    print(data_to_KLD(companies_def,companies_nondef,i))
    if data_to_KLD(companies_def,companies_nondef,i) > 0:
        kld_val.append(data_to_KLD(companies_def,companies_nondef,i))
    else:
        kld_val.append(0)

fig1, ax = plt.subplots()
ax.bar(np.arange(3,40),kld_val)
plt.show()
plt.close()
import numpy as np
import scipy
import matplotlib.pyplot as plt
import csv
import statistics

###
### Zebranie danych, podstawowe definicje
###

def printsci(str):
    print("{:e}".format(str))

def flornone(x):
    if x == 'NA':
        return None
    else:
        return float(x)

with open(".\credit_sample.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = []
    for i in range(100000):#148900
        data_read.append(next(reader))
    # data_read = [row for row in reader]

data_read = data_read[1:]

Vars = [i[2:-1] for i in data_read]
Vars = [[float(lis[i]) for lis in Vars[1:] if not lis[i]=='NA'] for i in range(39)]

AssetsCritValue = np.percentile(Vars[0],98)
# print(AssetsCritValue)
# data_read = [i for i in data_read[1:] if float(i[2])<AssetsCritValue]
# print(data_read[0])

###
### Histogram
###

def reject_outliers(data, m = 2.):
    data = np.array([i for i in data if i != None])
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zero(len(d))
    return data[s<m]

def showhistogram(var,nbins,rejectvalue,var2=None,rv2=2):
    varrejected = reject_outliers(np.array(var), rejectvalue)
    hist = np.histogram(varrejected, nbins)
    # print(hist[1])
    
    fig1, ax = plt.subplots()
    ax.bar(hist[1][:-1], hist[0], width=np.diff(hist[1]), edgecolor="blue", align="edge",alpha=0.8)
    if var2 != None:
        varrejected2 = reject_outliers(np.array(var2), rv2)
        hist2 = np.histogram(varrejected2, nbins)
        ax.bar(hist2[1][:-1], hist2[0], width=np.diff(hist2[1]), edgecolor="orange", align="edge",alpha=0.8)

    plt.show()
    plt.close(fig1)    

# showhistogram(Vars[4], 100, 2)

###
### Korelacja wskaźnika z danymi 0/1
###

### Wskaźnik "on itself" - pewna funkcja probabilistyczna zmiennych Var_i

### Na dobry początek same zmienne
def W(i,var):
    k = 2.3/np.sqrt(statistics.variance(Vars[i]))
    return 1/(1+np.exp(-k*(var-np.percentile(Vars[i],98))))
### To trzeba zrobić bardziej optymalnie z tym k

# for j in range(100):
#     print(W(1,Vars[1][j]))

## Coś tam se chodzi, ta zależność jeszcze nie jest jakaś przemyślana

### Korelacje z 0/1

companies = {}
id_now = "0"

for line in data_read:
    if id_now != line[0]:
        id_now = line[0]
        companies[id_now] = [line[1:]]
    else:
        companies[id_now].append(line[1:])

companies_def = {k:v for (k,v) in companies.items() if True in [bool(int(val[-1])) for val in companies[k]]}
companies_nondef = {k:v for (k,v) in companies.items() if not (True in [bool(int(val[-1])) for val in companies[k]])}

# print(companies_def)
# print(companies_nondef)

# print(len(companies_def))
# print(len(companies_nondef))

### Sort by date

companies_def = {k:sorted(v,key=lambda l: l[0]) for (k,v) in companies_def.items()}
# print(companies_def)
companies_nondef = {k:sorted(v,key=lambda l: l[0]) for (k,v) in companies_nondef.items()}
# print(companies_nondef)

def catch(val,i):
    try:
        return flornone(val[i][36])
    except:
        return None


vardictdef = [catch(val,i) for val in companies_def.values() for i in range(len(val))]
vardictdef = [i for i in vardictdef if i != None]
vardictnondef = [catch(val,i) for val in companies_nondef.values() for i in range(len(val))]
vardictnondef = [i for i in vardictnondef if i != None]

print(len(vardictdef))
print(len(vardictnondef))

print(statistics.median(vardictdef))
print(statistics.median(vardictnondef))

showhistogram(vardictdef,100,70,var2=vardictnondef,rv2=1.5)

fig1, ax = plt.subplots()
ax.plot([i for i in range(len(companies_def['96135545']))],[catch(companies_def['96135545'],i) for i in range(len(companies_def['96135545']))])
plt.show()
plt.close(fig1)


# print(companies)


### Kullback–Leibler divergence



example1 = [0,0,1,2,3,4,4,3,2,1,0,0,0,0,0,0,0]
example2 = [0,0,0,0,0,0,0,0,1,1,2,2,3,3,3,3,2]

def KLD(data0,data1):
    data1 = data1 / scipy.linalg.norm(data1,order=1)
    data0 = data0 / scipy.linalg.norm(data0,order=1)
    kld_data = []
    for i in range(len(example1)):
        kld_data.append(data1[i]*np.log(data1[i]/data0[i]))
    return sum(kld_data)

print(KLD(example1,example2))
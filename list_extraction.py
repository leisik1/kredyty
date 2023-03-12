# import numpy as np
# import scipy
# import matplotlib.pyplot as plt
# import csv
# import statistics

# with open("sorted_data.csv") as fp:
#     reader = csv.reader(fp, delimiter=";", quotechar='"')
#     data_read = []
#     for i in range(100000):#148900
#         data_read.append(next(reader))

# companies = {}
# id_now = "0"

# for line in data_read:
#     if id_now != line[0]:
#         id_now = line[0]
#         companies[id_now] = [line[1:]]
#     else:
#         companies[id_now].append(line[1:])

# companies_def = {k:v for (k,v) in companies.items() if True in [bool(int(val[-1])) for val in companies[k]]}
# companies_nondef = {k:v for (k,v) in companies.items() if not (True in [bool(int(val[-1])) for val in companies[k]])}

# print(companies_def)

import csv 


id_and_def = {}

# with open("sorted_data.csv") as file:
#     output = csv.reader(file, delimiter=";", quotechar='"')
#     for row in output:
#         if row[0] not in id_and_def.keys():
#             id_and_def[row[0]] = []
#             id_and_def[row[0]].append(row[-1])
#         else:
#             id_and_def[row[0]].append(row[-1])

# with open("sorted_data.csv") as file:
#     output = csv.reader(file, delimiter=";", quotechar='"')
#     for row in output:
#         if row[0] not in id_and_def.keys():
#             id_and_def[row[0]] = []
#             for val in range(42):
#                 id_and_def[row[0]].append(row[val])
#         else:
#             for val in range(42):
#                 id_and_def[row[0]].append(row[val])

# file.close()

# print(id_and_def["2897"])

###WS

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
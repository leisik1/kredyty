import pandas as pd

data_frame = pd.read_table("sorted_data.csv", delimiter=";")

#Sorted data CSV has two depth sort - first the ID and second the Date from oldest to newest

print(data_frame.loc[1:3, ['ID', 'default']])
 

groups = data_frame['ID'].unique()
subsets = {}

for group in groups:
    name = "ID" + str(group)
    subsets[name] = data_frame[data_frame['ID'] == group]

print(subsets["ID9353"])

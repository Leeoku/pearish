import pandas as pd
import numpy as np 


ks = pd.read_excel('food.xlsx')

ks.head(100)


mst_common = []
shrt = ks['Long_Desc'].tolist()

# for item in shrt:
#     item = item.split(',')
#     for i in item: 
#         mst_common[i] = mst_common.get(i, 0) + 1
    
# sort_items = sorted(mst_common.items(), key=lambda x: x[1], reverse=True)

# print(len(mst_common))

# sort_items

for item in shrt : 
    item = item.split(',')
    mst_common.append(item[0].lower())

m = np.asarray(mst_common)
ks['Long_Desc'] = m  

ks.head()
 
set_word = set(mst_common)
import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 2
means_btree = (19, 5)
means_bms_tree = (54, 16)
#means_paillier_search = (4.1, 10)
 
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index, means_btree, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Binary Tree based Search')
 
rects2 = plt.bar(index + bar_width, means_bms_tree, bar_width,
                 alpha=opacity,
                 color='royalblue',
                 label='BMS Tree based Search')
 
#rects3 = plt.bar(index + 2 * bar_width, means_paillier_search, bar_width,
#                 alpha=opacity,
#                 color='mediumpurple',
#                 label='Paillier based Search')

plt.xlabel('Memory                                                                       CPU')
plt.ylabel('Percentage utilization')
plt.title('Memory/CPU Utilization')
plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
plt.legend()
 
plt.tight_layout()
plt.show()

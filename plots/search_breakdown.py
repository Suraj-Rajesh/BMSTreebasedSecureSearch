import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = ('Query hashing', 'Tree traversal', 'Query encrypt (M1iQ1, M2iQ2)', 'Scoring & ranking')
y_pos = np.arange(len(objects))
performance = [5.67, 55.29, 42.93, 1.05]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Time (in percent)')
plt.title('Search Breakdown')
 
plt.show()

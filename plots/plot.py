from matplotlib import pyplot as plt
from matplotlib import style

style.use('ggplot')

#x = [5,8,10]
#y = [12,16,6]

x = list()
y = list()
x2 = list()
y2 = list()
x3 = list()
y3 = list()

with open("search_terms.txt") as f:
    for line in f:
        x.append(float(line.split()[0]))
        y.append(float(line.split()[1]))

with open("search_terms_BMS.txt") as f:
    for line in f:
        x2.append(float(line.split()[0]))
        y2.append(float(line.split()[1]))


with open("search_terms_paillier.txt") as f:
    for line in f:
        x3.append(float(line.split()[0]))
        y3.append(float(line.split()[1]))

plt.plot(x,y,linewidth=5)
plt.plot(x2,y2,linewidth=5)
plt.plot(x3,y3,linewidth=5)

plt.title('Search Performance')
plt.ylabel('Time (ms)')
plt.xlabel('Query terms')

plt.show()

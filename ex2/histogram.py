import numpy as np
import matplotlib.pyplot as plt

a = np.fromfile("data/slice.1", dtype=np.dtype(np.ushort))
for i in range(2, 95):
    a = np.hstack((a, np.fromfile("data/slice.%d" % i, dtype=np.dtype(np.ushort))))

hist, bins = np.histogram(a, bins=65536)
hist[0] = 0

plt.bar(range(2500), hist[:2500], align='center')
plt.show()
#print hist

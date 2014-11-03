import matplotlib.pyplot as plt


plt.plot([0], [0], 'bo') # red circle
plt.plot([0], [1], 'rs') # green square
plt.plot([0], [2], 'gp')
plt.plot([1], [0], 'gh')
plt.plot([1], [1], 'g8') # ?
plt.plot([1], [2], 'o', color='#0000FF') # hexastring circle
plt.plot([2], [0], 'o', color='#0000FF', markersize=2) # hexastring circle
plt.plot([2], [1], 'o', color='#0000FF', markersize=6) # hexastring circle
plt.plot([2], [2], 'o', color='#0000FF', markersize=16) # hexastring circle
plt.axis([-.5, 3.5, -.5, 3.5])
plt.show()

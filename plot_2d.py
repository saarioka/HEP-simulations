import os
import matplotlib.pyplot as plt
import numpy as np

img = np.fromfile('si-900-1330-97.bnn')
img = img[:8000000].reshape([2**9, 5**6])
print(img.shape)
plt.imshow(img)
plt.show()

'''
with open('cdte-1000-30-97.bnn', 'rb') as f:
    byte = f.read(1)
    while byte:
        print(byte)
        byte = f.read(1)
'''

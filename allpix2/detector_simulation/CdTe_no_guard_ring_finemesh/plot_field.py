#!/usr/bin/python3

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from mayavi import mlab
from tqdm import tqdm

def main():
    data = []
    with open(os.path.join('.',sys.argv[1])) as f:
        lines = f.readlines()
    for l in lines[5:]:
        data.append(l.split())
    data = np.array(data).astype(float)
    magnitude = np.linalg.norm(data[:,3:], axis=1)
    mlab.figure('DensityPlot')
    #mlab.points3d(data[:,0], data[:,1], data[:,2], magnitude, scale_mode='none', scale_factor=0.2)
    mlab.quiver3d(data[:,0], data[:,1], data[:,2], data[:,3], data[:,4], data[:,5],
                  line_width=2)
    mlab.axes()
    mlab.show()
    '''
    plt.figure()
    print(data.shape)
    if data.shape[1] == 6: # vector quantity (electric field)
        magnitude = np.reshape(magnitude, (25, 17, 92), 'C')
        for i in tqdm(range(magnitude.shape[2])):
            plt.imshow(magnitude[:,:,i])
            plt.savefig(os.path.join('pics',f'slice_{i}.png'))
    '''

if __name__ == '__main__':
    main()

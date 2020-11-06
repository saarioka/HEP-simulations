import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

files = [f for f in os.listdir('.') if os.path.isfile(f) and '.dat' in f and 'doslev' not in f]

file2folder = {
    '96':'pics_displacement',
    '97':'pics_energy_deposit'
}

if not os.path.exists('pics_displacement'):
    os.makedirs('pics_displacement')

if not os.path.exists('pics_energy_deposit'):
    os.makedirs('pics_energy_deposit')

failed = []
for f in tqdm(files):
    img = np.genfromtxt(f)
    fig = plt.figure()
    if len(img[:,3]) == 40401:
        plt.imshow(img[:,2].reshape(201,201).transpose(), cmap='jet')
        plt.colorbar()
        fn = f.split('.')[0]

        plt.savefig(file2folder[fn.split('-')[-1]] + os.path.sep + fn + '.png')
        plt.close(fig)
    else:
        failed.append(f)

if len(failed) > 0:
    print('Conversion for following files failed:\n', failed)

import os
import numpy as np
import subprocess

logfile = open('convert.log', 'a+')
files = [f for f in os.listdir('.') if '.bnn' in f and '.lis' not in f]
for f in files:
    filename = f'{f}\n{f}.lis\n'
    subprocess.run(['usbrea'], input=bytes(filename, 'utf-8'), stdout=logfile)
    data = np.fromfile(f+'.lis')
    print(data.shape)

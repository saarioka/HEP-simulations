import numpy as np

filename = 'xcom_energies'
energies = np.linspace(1,1500,100)

with open(filename, 'w+') as f:
    for e in range(len(energies)):
        f.write(f'{float(energies[e]/1000)}\n')

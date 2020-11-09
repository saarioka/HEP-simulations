import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

fluence_bins = 150

files = [f[:-11] for f in os.listdir('.') if os.path.isfile(f) and ('si-' in f or 'cdte-' in f or 'cdteneutron-' in f) and '-21_tab.lis' in f and 'versio' not in f]

if not os.path.exists(os.path.join('.', 'pics_fluences')):
    os.makedirs('pics_fluences')

for f in tqdm(files):
    fig = plt.figure()
    bulk, thickness, energy= f.split('-')
    if bulk == 'cdteneutron':
        plt.title(f'Particle fluence: {thickness}$\mu$m CdTe bulk, {energy}keV neutron beam')
    elif bulk == 'cdte':
        plt.title(f'Particle fluence: {thickness}$\mu$m CdTe bulk, {energy}keV photon beam')
    elif bulk == 'si':
        plt.title(f'Particle fluence: {thickness}$\mu$m silicon bulk, {energy}keV photon beam')

    data3 = pd.read_csv(f+'-94_tab.lis', sep='  ', skiprows=2, nrows=fluence_bins, engine='python').to_numpy()
    data3[:,0] = data3[:,0] * 1e6
    plt.fill_between(data3[:,0], data3[:,2], step='pre', alpha=0.3, color='tab:blue')

    data = pd.read_csv(f+'-21_tab.lis', sep='  ', skiprows=2, nrows=fluence_bins, engine='python').to_numpy()
    data[:,0] = data[:,0] * 1e6
    plt.fill_between(data[:,0], data[:,2], step='pre', color='tab:green')

    data2 = pd.read_csv(f+'-22_tab.lis', sep='  ', skiprows=2, nrows=fluence_bins, engine='python').to_numpy()
    data2[:,0] = data2[:,0] * 1e6
    plt.fill_between(data2[:,0], data2[:,2], step='pre', alpha=0.5, color='tab:orange')

    plt.plot(data3[:,0], data3[:,2], drawstyle='steps', linewidth=0.3, color='tab:blue', label='Inside bulk')
    plt.plot(data2[:,0], data2[:,2], drawstyle='steps', linewidth=0.5, color='tab:orange', label='Boundary crossing from bulk to surface passivation layer')
    plt.plot(data[:,0], data[:,2], drawstyle='steps', linewidth=0.5, color='tab:green', label='Boundary crossing from metal to bulk')

    plt.xlim(10, 1400)
    plt.ylim(10, 1e10)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Particle energy [keV]')
    plt.ylabel('Fluence [dn/dE]')
    plt.grid()
    plt.legend(title='Fluence type', loc="upper left", fontsize='small')
    plt.tight_layout()
    plt.savefig(os.path.join('.', 'pics_fluences', f))
    plt.close(fig)


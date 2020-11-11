import os, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import colors
import output_processing

output_processing.process_USRBIN()

data = pd.read_csv('energy_and_displacements.csv')
plot_colors = ['tab:blue', 'tab:red', 'tab:green']
bulknames = ['si', 'cdte', 'cdteneutron']
legendnames = ['Silicon', 'CdTe, photon beam', 'CdTe, neutron beam']
plt.figure(figsize=[9,5.5])
for b in range(len(bulknames)):
    d = data[data['Material'] == bulknames[b]]
    d = d.sort_values('Energy')
    plt.fill_between(d['Energy'], d['Displacements'], label=legendnames[b], step='pre', alpha=.5, facecolor=plot_colors[b])
plt.xlabel('Beam energy [keV]')
plt.ylabel('Displacements per atom')
plt.grid()
plt.yscale('log')
plt.legend(loc='upper left')
plt.title('Radiation damage (displacements per atom)')
plt.tight_layout()
plt.savefig(os.path.join('pics', 'displacements.png'))

plt.figure(figsize=[9,5.5])
for b in range(len(bulknames)):
    d = data[data['Material'] == bulknames[b]]
    d = d.sort_values('Energy')
    plt.fill_between(d['Energy'], d['Energydeposit'], label=legendnames[b], step='pre', alpha=.5, facecolor=plot_colors[b])
plt.xlabel('Beam energy [keV]')
plt.ylabel(r'Energy Density [$keV/cm^3$]')
plt.grid()
plt.yscale('log')
plt.legend(loc='center right')
plt.title('Deposited energy per volume')
plt.tight_layout()
plt.savefig(os.path.join('pics', 'deposited_energies.png'))
plt.show()


files = [f for f in os.listdir('.') if os.path.isfile(f) and '.dat' in f and 'doslev' not in f]
#files = sorted(files)

if not os.path.exists('pics_displacement'):
    os.makedirs('pics_displacement')

if not os.path.exists('pics_energy_deposit'):
    os.makedirs('pics_energy_deposit')

failed = []
#for f in tqdm(files):
for f in files[:3]:
    img = np.genfromtxt(f)
    if len(img[:,3]) == 40401:
        img = img[:,2].reshape(201,201).transpose()
        img[img == 0] = sys.float_info.min

        fn = f.split('.')[0]
        bulk, bt, energy, unit = fn.split('-')

        fig = plt.figure(figsize=(11,8))
        if unit == '96':
            # displacements
            h = plt.imshow(img,
                       cmap='gnuplot',
                       extent=[0, int(bt), -50, 50],
                       aspect=int(bt)/100,
                       norm=colors.LogNorm(vmin=1e-25, vmax=1e-16)
                       )
            h.cmap.set_under('k')
            h.cmap.set_over('w')
            plt.colorbar(extend='both')
            plt.xlabel(r'x [$\mu m$]')
            plt.ylabel(r'y [$\mu m$]')
            if bulk == 'si':
                plt.title(fr'Displacements per atom: {bt}$\mu$m silicon bulk, {energy} keV photon beam')
            elif bulk == 'cdte':
                plt.title(fr'Displacements per atom: {bt}$\mu$m CdTe bulk, {energy} keV photon beam')
            elif bulk == 'cdteneutron':
                plt.title(fr'Displacements per atom: {bt}$\mu$m CdTe bulk, {energy} keV neutron beam')
            plt.tight_layout()
            try:
                plt.savefig('pics_displacement' + os.path.sep + fn + '.png')
            except ValueError:
                print('Displacements: could not save ', fn)
                failed.append(f)

        if unit == '97':
            # energy deposit
            h = plt.imshow(img,
                       cmap='gnuplot',
                       extent=[0, int(bt), -50, 50],
                       aspect=int(bt)/100,
                       norm=colors.LogNorm(vmin=1e-7, vmax=1e3)
                       )
            h.cmap.set_under('k')
            h.cmap.set_over('y')
            plt.colorbar(extend='both')
            plt.xlabel(r'x [$\mu m$]')
            plt.ylabel(r'y [$\mu m$]')
            plt.title('Energy deposition')
            if bulk == 'si':
                plt.title(fr'Energy deposition: {bt}$\mu$m silicon bulk, {energy} keV photon beam')
            elif bulk == 'cdte':
                plt.title(fr'Energy deposition: {bt}$\mu$m CdTe bulk, {energy} keV photon beam')
            elif bulk == 'cdteneutron':
                plt.title(fr'Energy deposition: {bt}$\mu$m CdTe bulk, {energy} keV neutron beam')
            try:
                plt.savefig(os.path.join('pics_energy_deposit', fn + '.png'))
            except ValueError:
                print('Energy deposit: could not save ', fn)
                failed.append(f)
            plt.tight_layout()

        plt.close(fig)
    else:
        failed.append(f)

if len(failed) > 0:
    print('Conversion for following files failed:\n', failed)
plt.show()

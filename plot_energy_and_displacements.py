import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from matplotlib import colors
import output_processing

output_processing.process_USRBIN()

files = [f for f in os.listdir('.') if os.path.isfile(f) and '.dat' in f and 'doslev' not in f]
#files = sorted(files)

if not os.path.exists('pics_displacement'):
    os.makedirs('pics_displacement')

if not os.path.exists('pics_energy_deposit'):
    os.makedirs('pics_energy_deposit')

failed = []
for f in tqdm(files):
#for f in files[:10]:
    img = np.genfromtxt(f)
    if len(img[:,3]) == 40401:
        img = img[:,2].reshape(201,201).transpose()
        img[img < 1e-27] = 0 # outside numerical accuray... creates noise in plots

        fn = f.split('.')[0]
        bulk, bt, energy, unit = fn.split('-')

        fig = plt.figure(figsize=(11,8))
        if unit == '96':
            # displacements
            plt.imshow(img,
                       cmap='jet',
                       extent=[0, int(bt), -50, 50],
                       aspect=int(bt)/100,
                       #norm=colors.LogNorm(vmin=1e-29, vmax=1e-20)
                       )
            plt.colorbar()
            plt.xlabel(f'x [$\mu m$]')
            plt.ylabel(f'y [$\mu m$]')
            if bulk == 'si':
                plt.title(f'Displacements per atom: {bt}$\mu$m silicon bulk, {energy} keV photon beam')
            elif bulk == 'cdte':
                plt.title(f'Displacements per atom: {bt}$\mu$m CdTe bulk, {energy} keV photon beam')
            elif bulk == 'cdteneutron':
                plt.title(f'Displacements per atom: {bt}$\mu$m CdTe bulk, {energy} keV neutron beam')
            plt.tight_layout()
            try:
                plt.savefig('pics_displacement' + os.path.sep + fn + '.png')
            except ValueError:
                print('Could not save ', fn)
                failed.append(f)

        if unit == '97':
            # energy deposit
            plt.imshow(img,
                       cmap='jet',
                       extent=[0, int(bt), -50, 50],
                       aspect=int(bt)/100,
                       norm=colors.LogNorm(vmin=1e-6, vmax=25)
                       )
            plt.colorbar()
            plt.xlabel(f'x [$\mu m$]')
            plt.ylabel(f'y [$\mu m$]')
            plt.title('Energy deposition')
            if bulk == 'si':
                plt.title(f'Energy deposition: {bt}$\mu$m silicon bulk, {energy} keV photon beam')
            elif bulk == 'cdte':
                plt.title(f'Energy deposition: {bt}$\mu$m CdTe bulk, {energy} keV photon beam')
            elif bulk == 'cdteneutron':
                plt.title(f'Energy deposition: {bt}$\mu$m CdTe bulk, {energy} keV neutron beam')
            try:
                plt.savefig(os.path.join('pics_energy_deposit', fn + '.png'))
            except ValueError:
                print('Could not save ', fn)
                failed.append(f)
            plt.tight_layout()

        plt.close(fig)
    else:
        failed.append(f)

if len(failed) > 0:
    print('Conversion for following files failed:\n', failed)
plt.show()

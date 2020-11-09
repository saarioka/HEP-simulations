import os, sys
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
                print('Energy deposit: could not save ', fn)
                failed.append(f)
            plt.tight_layout()

        plt.close(fig)
    else:
        failed.append(f)

if len(failed) > 0:
    print('Conversion for following files failed:\n', failed)
plt.show()

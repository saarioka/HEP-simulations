import os, sys, copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
from tqdm import tqdm
from matplotlib import colors
import output_processing

output_processing.process_USRBIN()

bulks_si = list(range(320, 901, 58))
bulks_cdte = list(range(1000, 2001, 100))
energies = list(range(30, 1331, 50))

data_all = pd.read_csv('energy_and_displacements.csv')
si = data_all[data_all['Material'] == 'si']
cdte = data_all[data_all['Material'] == 'cdte']
cdteneutron = data_all[data_all['Material'] == 'cdteneutron']

bulknames = ['si', 'cdte', 'cdteneutron']

def plot_displacements(results, bulk, identifier, normalization_factor, colorlist, ylim=[0,5e3]):
    for b in range(len(bulk)):
        data = results[results['Thickness'] == bulk[b]]
        data = data.sort_values('Energy')
        plt.plot(data['Energy'], data['Displacements'] / normalization_factor[b], label=str(bulk[b]) + r'$\mu m$ ' + identifier, color=colorlist[b])
    plt.xlabel('Beam energy [keV]')
    #plt.ylabel('Displacements per atom')
    plt.ylabel(r'Displacements/$cm³$')
    plt.grid()
    plt.xlim(30, 1300)
    plt.ylim(ylim)
    plt.yscale('log')
    plt.legend(fontsize='x-small', loc="center right", ncol=3, bbox_to_anchor=(1, 0.46))
    plt.title('Radiation damage')
    plt.tight_layout()
    plt.savefig(os.path.join('pics', 'displacements.png'))

def plot_energy_depositions(results, bulk, identifier, normalization_factor, colorlist, ylim=[1,5e3]):
    for b in range(len(bulk)):
        data = results[results['Thickness'] == bulk[b]]
        data = data.sort_values('Energy')
        plt.plot(data['Energy'], data['Energydeposit'] / normalization_factor[b], label=str(bulk[b]) + r'$\mu m$ ' + identifier, color=colorlist[b])
    plt.xlabel('Beam energy [keV]')
    plt.ylabel(r'Energy Density [$keV/cm^3$]')
    plt.grid()
    plt.xlim(30, 1300)
    plt.ylim(ylim)
    plt.yscale('log')
    plt.legend(fontsize='x-small', loc="lower right", ncol=3)
    plt.title('Deposited energy per volume')
    plt.tight_layout()
    plt.savefig(os.path.join('pics', 'deposited_energies.png'))

# NOTE: only works if the scored region covers the bulk onlcovers the bulk only
# N = N_A * n
# N = N_A * V*rho/M
# N = N_A * width*height*depth * rho / M
#atoms_per_bulk_si = 6.0221415e23 * 100e-4*150e-4*np.array(bulks_si)*1e4 * 2.3290 / 28.08553
#atoms_per_bulk_cdte = 6.0221415e23 * 100e-4*150e-4*np.array(bulks_cdte)*1e4 * 5.85 / 240.01

# works despite linter error (pylint)
# https://github.com/PyCQA/pylint/issues/2289
colorlist = plt.cm.turbo(np.linspace(0,1,3*len(bulks_si)))

pixel_volume_si = 100e-4*150e-4*np.array(bulks_si)*1e4
pixel_volume_cdte = 100e-4*150e-4*np.array(bulks_cdte)*1e4

plt.figure(figsize=[11,7])
plot_displacements(si, bulks_si, 'Si', pixel_volume_si, colorlist[:11])
plot_displacements(cdte, bulks_cdte, r'CdTe ($\gamma$)', pixel_volume_cdte, colorlist[11:22])
plot_displacements(cdteneutron, bulks_cdte, 'CdTe (n)', pixel_volume_si, colorlist[22:33])

plt.figure(figsize=[11,7])
plot_energy_depositions(si, bulks_si, 'Si', pixel_volume_si, colorlist[:11])
plot_energy_depositions(cdte, bulks_cdte, r'CdTe ($\gamma$)', pixel_volume_cdte, colorlist[11:22])
plot_energy_depositions(cdteneutron, bulks_cdte, 'CdTe (n)', pixel_volume_si, colorlist[22:33])
plt.show()

files = [f for f in os.listdir('.') if os.path.isfile(f) and '.dat' in f and 'doslev' not in f]
#files = sorted(files)

if not os.path.exists('pics_displacement'):
    os.makedirs('pics_displacement')

if not os.path.exists('pics_energy_deposit'):
    os.makedirs('pics_energy_deposit')


cmap = copy.copy(mpl.cm.get_cmap('gnuplot'))
cmap.set_under('k')
cmap.set_over('w')

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
                       cmap=cmap,
                       extent=[0, int(bt), -50, 50],
                       aspect=int(bt)/100,
                       norm=colors.LogNorm(vmin=1e-25, vmax=1e-16)
                       )
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
                       cmap=cmap,
                       extent=[0, int(bt), -50, 50],
                       aspect=int(bt)/100,
                       norm=colors.LogNorm(vmin=1e-7, vmax=1e3)
                       )
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

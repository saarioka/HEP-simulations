import os
import glob
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

import read_fluences2

read_fluences2.create_csv('fluences2.csv') # update csv file
data = pd.read_csv('fluences2.csv')

bulks_si = list(range(320, 901, 58))
bulks_cdte = list(range(1000, 2001, 100))
energies = list(range(30, 1331, 50))

# mapping from filke indices to bulk thicknesses
ind2bulk_si = dict(zip(list(range(1, len(bulks_si)+1)), bulks_si))
ind2bulks_cdte = dict(zip(list(range(1, len(bulks_cdte)+1)), bulks_cdte))
ind2energies = dict(zip(list(range(1, len(energies)+1)), energies))

si = data[data['Material'] == 'si']
cdte = data[data['Material'] == 'cdte']

def plot_intensity(results, bulk, identifier, ylim=[0,1]):
    # works despite linter error (pylint)
    # https://github.com/PyCQA/pylint/issues/2289
    colors = plt.cm.turbo(np.linspace(0,1,len(bulks_si)))
    plt.figure(figsize=[7,5.5])
    for b in range(len(bulk)):
        data = results[results['Thickness'] == bulk[b]]
        data = data.sort_values('Energy')
        I0 = list(data['Fluence1'])
        I = list(data['Fluence2'])
        I0 = [i if i > 1 else np.nan for i in I0] # Fluence is about 7000 in the beginning -> most radiation is absorbed into aluminum if I<1
        I_pass = np.divide(I,I0)
        #rel_I = [i if not np.isnan(i) else 0 for i in rel_I]
        plt.plot(data['Energy'], I_pass, color=colors[b])
        plt.scatter(data['Energy'], I_pass, color=colors[b], marker='x', label=str(bulks_si[b]) + r' $\mu$m')
    plt.xlabel('Beam energy [keV]')
    plt.ylabel('$I/I_0$')
    plt.grid()
    plt.ylim(ylim)
    plt.legend(title='Bulk thickness', fontsize='small')
    plt.title('Beam intensity: ' + identifier)
    plt.savefig(identifier + '_fluence.png')

def plot_attenuation(results, identifier, ylim=[0,1]):
    colors = plt.cm.turbo(np.linspace(0,1,len(energies)))
    plt.figure(figsize=[10,5.5])
    for e in range(len(energies)):
        data = results[results['Energy'] == energies[e]]
        data = data.sort_values('Energy')
        I0 = list(data['Fluence1'])
        I = list(data['Fluence2'])
        I = [i if i > 1 else np.nan for i in I]
        rel_I = np.log(np.divide(I0,I))
        #rel_I = [i if not np.isnan(i) else 0 for i in rel_I]
        plt.plot(data['Thickness'], rel_I, color=colors[e])
        plt.scatter(data['Thickness'], rel_I, color=colors[e], marker='x', label=str(energies[e]) + ' keV')
    plt.xlabel(r'Bulk thickness [$\mu$m]')
    plt.ylabel('ln($I_0/I$)')
    plt.grid()
    plt.ylim(ylim)
    plt.legend(title='Beam energies', loc="upper left", ncol=2, fontsize='small', bbox_to_anchor=(1.05, 1))
    plt.title(' Plot of ln($I_0/I$) values versus thickness of attenuator medium ' + identifier)
    plt.savefig(identifier + '_attenuation.png')
    plt.tight_layout()


plot_intensity(si, bulks_si, 'Silicon', ylim=[0.95, 1])
plot_intensity(cdte, bulks_cdte, 'CdTe')

plot_attenuation(si, 'Silicon', ylim=[0, 0.05])
plot_attenuation(cdte, 'CdTe')

plt.show()

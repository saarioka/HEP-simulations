import os, sys
import glob
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from scipy.stats import linregress

import output_processing

output_processing.process_USRBDX('fluences2.csv')
data_all = pd.read_csv('fluences2.csv')

bulks_si = list(range(320, 901, 58))
bulks_cdte = list(range(1000, 2001, 100))
energies = list(range(30, 1331, 50))

# mapping from file indices to bulk thicknesses
ind2bulk_si = dict(zip(list(range(1, len(bulks_si)+1)), bulks_si))
ind2bulks_cdte = dict(zip(list(range(1, len(bulks_cdte)+1)), bulks_cdte))
ind2energies = dict(zip(list(range(1, len(energies)+1)), energies))

si = data_all[data_all['Material'] == 'si']
cdte = data_all[data_all['Material'] == 'cdte']
cdteneutron = data_all[data_all['Material'] == 'cdteneutron']


xcom_si = pd.read_csv('xcom_si', skiprows=2, engine='python', sep=' ').to_numpy()
xcom_cdte = pd.read_csv('xcom_cdte', skiprows=2, engine='python', sep=' ').to_numpy()

xcom_si[xcom_si == 0] = np.nan
xcom_cdte[xcom_cdte == 0] = np.nan

xcom_si[:,0] *= 1e3 # to keV
xcom_cdte[:,0] *= 1e3

xcom_si[:,6] *= 2.3290 # multiply by density to get µ
xcom_cdte[:,6] *= 5.85

if not os.path.exists(os.path.join('.', 'pics')):
    os.makedirs('pics')

def plot_intensity(results, bulk, identifier, ylim=[0,1]):
    # works despite linter error (pylint)
    # https://github.com/PyCQA/pylint/issues/2289
    colors = plt.cm.turbo(np.linspace(0,1,len(bulks_si)))

    plt.figure(figsize=[9,5.5])
    for b in range(len(bulk)):
        data = results[results['Thickness'] == bulk[b]]
        data = data.sort_values('Energy')
        I0 = list(data['Fluence1'])
        I = list(data['Fluence2'])
        I0 = [i if i > sys.float_info.epsilon else np.nan for i in I0] # Fluence is about 7000 in the beginning
        I_pass = np.divide(I,I0)
        plt.plot(data['Energy'], I_pass, color=colors[b])
        plt.scatter(data['Energy'], I_pass, color=colors[b], marker='x', label=str(bulk[b]) + r' $\mu m$')
    plt.xlabel('Beam energy [keV]')
    plt.ylabel('$I/I_0$')
    plt.grid()
    plt.ylim(ylim)
    plt.legend(title='Bulk thickness', fontsize='small', loc="upper left", bbox_to_anchor=(1, 1))
    plt.title('Beam intensity: ' + identifier)
    plt.tight_layout()
    plt.savefig(os.path.join('pics',identifier + '_fluence.png'))

def plot_attenuation(results, identifier, ylim=[0,1]):
    colors = plt.cm.turbo(np.linspace(0,1,len(energies)))
    coeffs = []
    plt.figure(figsize=[10,6.5])
    for e in range(len(energies)):
        data = results[results['Energy'] == energies[e]]
        data = data.sort_values('Energy')
        I0 = list(data['Fluence1'])
        I = list(data['Fluence2'])
        I = [i if i > sys.float_info.epsilon else np.nan for i in I]
        rel_I = np.log(np.divide(I0,I))
        plt.scatter(data['Thickness'], rel_I, color=colors[e], marker='x')
        fit = linregress(data['Thickness'], rel_I)
        plt.plot(data['Thickness'], data['Thickness']*fit.slope + fit.intercept, color=colors[e], label=f'{energies[e]:4}keV: CC={fit.rvalue:.3e}, SE={fit.stderr:.1e}')
        coeffs.append(fit.slope) # [µ]=1/µm
    plt.xlabel(r'Bulk thickness [$\mu m$]')
    plt.ylabel('ln($I_0/I$)')
    plt.grid()
    plt.ylim(ylim)
    plt.legend(title='Beam energies with linear fits,\n fit correlation coefficients (CC)\nand standard errors (SE)', loc="upper left", fontsize='small', bbox_to_anchor=(1, 1))
    plt.title('Plot of ln($I_0/I$) values versus thickness of attenuator medium: ' + identifier)
    plt.tight_layout()
    plt.savefig(os.path.join('pics', identifier + '_attenuation.png'))
    return np.array(coeffs)

def plot_coefficients(results, coeffs, xcom, bulk, identifier, ylim=[0.1, 20]):
    colors = plt.cm.turbo(np.linspace(0,1,len(energies)))
    plt.figure(figsize=[7,5.5])
    plt.plot(xcom[:,0], xcom[:,6], c='tab:blue', label='XCOM data')
    plt.scatter(energies, coeffs * 1e4, s=50, c='tab:red', marker='x', label='Computed from simulation results') # multiply by 1e4 to convert from µm to cm
    plt.xlabel(r'Beam energy [keV]')
    plt.ylabel(r'$\mu$ [$cm^{-1}$]')
    plt.grid()
    plt.xlim([70, 1500])
    plt.ylim(ylim)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(loc="upper right")
    plt.title('Linear attenuation coefficients: ' + identifier)
    plt.tight_layout()
    plt.savefig(os.path.join('pics', identifier + '_attenuation_coef.png'))

plot_intensity(si, bulks_si, 'Silicon', ylim=[0.95, 1])
plot_intensity(cdte, bulks_cdte, 'CdTe (photon beam)')
plot_intensity(cdteneutron, bulks_cdte, 'CdTe (neutron beam)', ylim=[0.95, 1])

coeffs_si = plot_attenuation(si, 'Silicon', ylim=[2e-3, 0.05])
coeffs_cdte = plot_attenuation(cdte, 'CdTe (photon beam)')
plot_attenuation(cdteneutron, 'CdTe (neutron beam)', ylim=[0.015, 0.045])

plot_coefficients(si, coeffs_si, xcom_si, bulks_si, 'Silicon', ylim=[0.1, 0.65])
plot_coefficients(cdte, coeffs_cdte, xcom_cdte, bulks_cdte, 'CdTe (photon beam))')

plt.show()

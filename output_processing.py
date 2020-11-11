import os
import csv
import subprocess
from tqdm import tqdm
import numpy as np
import pandas as pd

def process_USRBDX(filename):
    files1 = [f for f in os.listdir('.') if os.path.isfile(f) and ('si-' in f or 'cdte-' in f or 'cdteneutron-' in f) and '-21_sum.lis' in f and 'versio' not in f]
    files2 = [f for f in os.listdir('.') if os.path.isfile(f) and ('si-' in f or 'cdte-' in f or 'cdteneutron-' in f) and '-22_sum.lis' in f and 'versio' not in f]

    files1 = sorted(files1)
    files2 = sorted(files2)

    print(f'USRBDX: found {len(files1)} and {len(files2)} files')

    with open(filename, 'w+') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Filename', 'Material', 'Thickness', 'Energy', 'Fluence1', 'Fluence1 error (%)', 'Fluence2', 'Fluence2 error (%)'])

        for n in range(len(files1)):
            f1 = open(files1[n], 'r')
            f2 = open(files2[n], 'r')
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            fluence1 = lines1[15].split()[3]
            fluence2 = lines2[15].split()[3]
            error1 = lines1[15].split()[5]
            error2 = lines2[15].split()[5]
            params = files1[n].split('-')

            writer.writerow(['-'.join(files1[n].split('-')[:3]), params[0], params[1], params[2], fluence1, error1, fluence2, error2])

def process_USRBIN():
    '''
    First pass: Preprocess the binary files with gplevbin
    '''
    logfile = open('convert_usrbin.log', 'a+')
    files_all = [f for f in os.listdir('.') if os.path.isfile(f) and ('si-' in f or 'cdte-' in f or 'cdteneutron-' in f)]
    files_todo = [f for f in files_all if '.bnn' in f and 'versio' not in f and f.split('.')[0]+'.dat' not in files_all]
    print(f'USRBIN: found {len(files_todo)} to process')
    failed = []
    for f in tqdm(files_todo):
        outfile = f.split('.')[0]+'.dat'
        subprocess.run(["gplevbin"], input=bytes(f"\n\n{f}\n\n\n1\n\n200\n\n1\n\n200\n\n", 'utf-8'), stdout=logfile)
        try: os.rename("gplevh.dat", outfile)
        except: failed.append(outfile)
    if len(failed) > 0:
        print('Conversion of following files failed:\n', failed)
    for fn in ("gplevh.lim", "gplevh.npo", "gplevh.poi", "doslev.dat", "fort.11", "fort.15"):
        try: os.remove(fn)
        except: pass

    datafilename = 'energy_and_displacements.csv'
    if os.path.isfile(datafilename):
        return
    '''
    Second pass: Calculate integrals from results of previous step
    '''
    files = [f for f in os.listdir('.') if os.path.isfile(f) and '-96.dat' in f and 'doslev' not in f]
    #data = pd.DataFrame(columns=['Filename', 'Material', 'Thickness', 'Energy', 'Displacements', 'Energydeposit'])
    with open(datafilename, 'w+') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Filename', 'Material', 'Thickness', 'Energy', 'Displacements', 'Energydeposit'])
        for f in tqdm(files):
            f2 = list(f)
            f2[-5] = '7'
            f2 = ''.join(f2)
            disp = np.genfromtxt(f)
            e = np.genfromtxt(f2)
            if len(disp[:,3]) == 40401 and len(e[:,3]) == 40401:
                params = f.split('.')[0].split('-')
                writer.writerow([f.split('.')[0], params[0], params[1], params[2], np.sum(disp), np.sum(e)])


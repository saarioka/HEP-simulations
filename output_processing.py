import os
import csv
import subprocess
from tqdm import tqdm

def process_USRBDX(filename):
    files1 = [f for f in os.listdir('.') if os.path.isfile(f) and ('cdte-' in f or 'si-' in f) and '-21_sum.lis' in f and 'versio' not in f]
    files2 = [f for f in os.listdir('.') if os.path.isfile(f) and ('cdte-' in f or 'si-' in f) and '-22_sum.lis' in f and 'versio' not in f]

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
    Preprocess the binary files with gplevbin
    '''
    logfile = open('convert_usrbin.log', 'a+')
    files_all = [f for f in os.listdir('.') if os.path.isfile(f) and ('cdte-' in f or 'si-' in f)]
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

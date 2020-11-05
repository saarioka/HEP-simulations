import os
import subprocess
from tqdm import tqdm

cycles = 5
bulks_si = list(range(320, 901, 58))
bulks_cdte = list(range(1000, 2001, 100))
energies = list(range(30, 1331, 50))

bulks_si = dict(zip(list(range(1, len(bulks_si)+1)), bulks_si))
bulks_cdte = dict(zip(list(range(1, len(bulks_cdte)+1)), bulks_cdte))
energies = dict(zip(list(range(1, len(energies)+1)), energies))

print('si thicknesses:', bulks_si)
print('cdte thicknesses', bulks_cdte)
print('energies', energies)

filenumber = '%03d' % cycles

#input_files = [f for f in os.listdir('.') if os.path.isfile(f) and (('si-' in f or 'cdte-' in f) and '.inp' in f and 'echo' not in f and '~' not in f)]
input_files = [f for f in os.listdir('.') if os.path.isfile(f) and (('cdte-' in f) and '.inp' in f and 'echo' not in f and '~' not in f)]
input_files = sorted(input_files)
print(len(input_files), ' input files found')

units = [21, 22, 94, 96, 97]
filetypes = ['.bnx', '.bnx', '.trk', '.bnn', '.bnn']
programs = ['usxsuw', 'usxsuw', 'ustsuw', 'usbsuw', 'usbsuw']

logfile = open('simulate.log', 'a+')

result_files = [f[:-11] for f in os.listdir('.') if os.path.isfile(f) and '_sum.lis' in f]
missing_cnt = 0
for fn in tqdm(input_files):
    fns = fn.split('-')
    found = False
    for f in result_files:
        if fns[0] + '-' + str(bulks_cdte[int(fns[1])]) + '-' + str(energies[int(fns[2].split('.')[0])])  in f:
            found = True
    if not found:
        print(fns[0] + '-' + str(bulks_cdte[int(fns[1])]) + '-' + str(energies[int(fns[2].split('.')[0])]))
        missing_cnt += 1
        subprocess.run(['/media/santeri/linux-storage/fluka/bin/rfluka', '-M', str(cycles), fn], stdout=logfile)

        for u in range(len(units)):
            binaries = [f for f in os.listdir('.') if os.path.isfile(f) and (('si-' in f or 'cdte-' in f) and '_fort.' + str(units[u]) in f)]
            binaries = sorted(binaries)

            fns = fn.split('-')
            bm = fns[0]
            if bm == 'si':
                bt = bulks_si[int(fns[1])]
            elif bm == 'cdte':
                bt = bulks_cdte[int(fns[1])]
            else:
                print('BAD MATERIAL')
                exit()
            e = energies[int(fns[2].split('.')[0])]

            outname = bm + '-' + str(bt) + '-' + str(e) + '-' + str(units[u]) + filetypes[u]
            command = '\n'.join(binaries) + '\n\n' + outname + '\n'
            subprocess.run([programs[u]], input=bytes(command, 'utf-8'), stdout=logfile)

        binaries = [f for f in os.listdir('.') if os.path.isfile(f) and '_fort.' in f]
        for b in binaries:
            os.remove(b)
print(f'Total of {missing_cnt} processed')

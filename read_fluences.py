import os
import csv

files1 = [f for f in os.listdir('.') if os.path.isfile(f) and ('cdte-' in f or 'si-' in f) and '21_sum.lis' in f and 'versio' not in f]
files2 = [f for f in os.listdir('.') if os.path.isfile(f) and ('cdte-' in f or 'si-' in f) and '22_sum.lis' in f and 'versio' not in f]

files1 = sorted(files1)
files2 = sorted(files2)

print(f'found {len(files1)} and {len(files2)} files')

with open('fluences2.csv', 'w+') as outfile:
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
        params = files1[n].split('_')

        writer.writerow(['_'.join(files1[n].split('_')[:3]), params[0], params[1], params[2], fluence1, error1, fluence2, error2])

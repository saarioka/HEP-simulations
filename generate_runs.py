import os
import subprocess

cycles = 2
filenumber = '%03d' % cycles

input_files = [f for f in os.listdir('.') if os.path.isfile(f) and (('si-' in f or 'cdte-' in f) and '.inp' in f and 'echo' not in f)]
input_files = sorted(input_files)
print(len(input_files), ' input files found')

units = [21, 22, 94, 96, 97]
filetypes = ['.bnx', '.bnx', '.trk', '.bnn', '.bnn']
programs = ['usxsuw', 'usxsuw', 'ustsuw', 'usbsuw', 'usbsuw']

for fn in input_files:
    subprocess.run(['nohup', '/media/santeri/linux-storage/fluka/bin/rfluka', '-M', str(cycles), fn])

    for u in range(len(units)):
        binaries = [f for f in os.listdir('.') if os.path.isfile(f) and (('si-' in f or 'cdte-' in f) and '_fort.' + str(units[u]) in f)]
        binaries = sorted(binaries)
        print(binaries)

        command = '\n'.join(binaries) + '\n' + '\n' + fn.split('.')[0] + '_' + str(units[u]) + filetypes[u] + '\n'
        subprocess.run([programs[u]], input=bytes(command, 'utf-8'))

    binaries = [f for f in os.listdir('.') if os.path.isfile(f) and '_fort.' in f]
    for b in binaries:
        os.remove(b)

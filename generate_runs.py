import os
import subprocess

def um_to_cm(a):
    return a/10000

def kev_to_gev(a):
    return a/1e6

infile = open('template.inp')
lines = infile.readlines()

#Si: thickness 320um - 900um, energies 30keV - 1331keV
for t in range(320, 901, 58):
    for e in range(30, 1331, 50):
        lines[5] = '#define BULK_THICKNESS ' + str(um_to_cm(t)) + '\n'
        lines[6] = '#define BEAM_ENERGY ' + str(kev_to_gev(e)) + '\n'
        lines[7] = '#define BULK_MATERIAL_SILICON\n'
        lines[8] = '!#define BULK_MATERIAL_CDTE\n'
        fn = 'dyn_si_' + str(t) + '_' + str(e) + '.inp'
        print(fn, t, e)
        outfile = open(fn, 'w+')
        outfile.writelines(lines)
        subprocess.call('/usr/bin/nohup /media/santeri/linux-storage/fluka/bin/rfluka -M 1 ' + fn, shell=True)


#CdTe: thickness 1mm - 2mm, energies 30keV - 1331keV
for t in range(1000, 2000, 58):
    for e in range(30, 1331, 50):
        lines[5] = '#define BULK_THICKNESS ' + str(um_to_cm(t)) + '\n'
        lines[6] = '#define BEAM_ENERGY ' + str(kev_to_gev(e)) + '\n'
        lines[7] = '!#define BULK_MATERIAL_SILICON\n'
        lines[8] = '#define BULK_MATERIAL_CDTE\n'
        fn = 'dyn_cdte_' + str(t) + '_' + str(e) + '.inp'
        print(fn, t, e)
        outfile = open(fn, 'w+')
        outfile.writelines(lines)
        subprocess.call('/usr/bin/nohup /media/santeri/linux-storage/fluka/bin/rfluka -M 1 ' + fn, shell=True)

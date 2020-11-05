import subprocess
import os

bulks = [
    "320um silicon bulk",
    "900um silicon bulk",
    "1mm CdTe bulk",
    "2mm CdTe bulk"
]

files = [f for f in os.listdir('.') if os.path.isfile(f) and (('si-' in f or 'cdte-' in f) and ('.bnx' in f or '.trk' in f or '.bnn' in f))]
print(len(files), ' files found')

bulks_si = list(range(320, 901, 58))
bulks_cdte = list(range(1000, 2001, 100))
energies = list(range(30, 1331, 50))

print('si:', bulks_si)
print('cdte', bulks_cdte)
print('energies', energies)


bulk_ids = ["si_320", "si_900", "cdte_1000", "cdte_2000"]
energies = ["30", "60", "478", "661", "1000", "1300"]

# Fluences
titles = [
    "Particle fluence entering bulk material: ",
    "Particle fluence leaving bulk material: ",
    "Particle fluence inside bulk material: "
]

fluka_units = [21, 22, 94]

for t in range(len(titles)):
    for b in range(len(bulks)):
        command = f"file_id='{fluka_units[t]}'; title_str='{titles[t] + bulks[b]}'; bulk_id='{bulk_ids[b]}'; energies='{' '.join(energies)}'"
        print(command)
        subprocess.call(["gnuplot", "-e", command, "plot_fluence.p"])
# Displacements and energy depositions

titles = [
    "Displacements per atom: ",
    "Deposited energy per volume: "
]

fluka_units = [96, 97, 95]

plot_commands = [
    "plot_displacements.p",
    "plot_energy_depositions.p"
]

for t in range(len(titles)):
    for b in range(len(bulks)):
        for e in energies:
            #preprocess the binary file with gplevbin
            subprocess.run(["gplevbin"], input=bytes(f"\n\n{bulk_ids[b]}_{e}_{fluka_units[t]}.bnn\n\n\n1\n\n200\n\n1\n\n200\n\n", 'utf-8'))
            command = f"title_str='{titles[t] + bulks[b]}, beam energy {e}keV'"
            print(command)
            subprocess.call(["gnuplot", "-e", command, plot_commands[t]])

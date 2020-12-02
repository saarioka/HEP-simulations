#!/bin/bash

mesh_plotter -f efield_n6_ElectricField.init -u V/cm -p xy -c 1
mesh_plotter -f efield_n6_ElectricField.init -u V/cm -p xy -c 99
mesh_plotter -f efield_n6_ElectricField.init -u V/cm -p yz
mesh_plotter -f efield_n6_ElectricField.init -u V/cm -p zx

#!/bin/bash

cd /media/santeri/linux-storage/allpix-squared/build
make clean && cmake .. && make -j4
cd -

./run_simulations.sh

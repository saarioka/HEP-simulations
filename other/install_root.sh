mkdir root_build root_install && cd root_build
cmake -DCMAKE_INSTALL_PREFIX=../root_install ../root_src
sudo cmake --build . -- install -j4
cd ..
pwd
source /media/santeri/linux-storage/root_install/bin/thisroot.sh

reset
set terminal png size 800,400
set output 'pics/'.title_str.'.png'
set title title_str
unset grid
set xlabel 'x [cm]'
set xtics
set ylabel 'y [cm]'
set ytics
set cblabel 'Displacements per atom'
set cbtics
unset logscale x
unset logscale y
unset logscale z
set logscale cb
set cbrange [1E-29:1E-21]
unset logscale x2
unset logscale y2
set key default

set style line 1 lt -1 lw 1
set cbrange [1e-29:1e-21]
set colorbox vertical
set pm3d map explicit corners2color c1
set palette defined ( 1. 1.0 1.0 1.0,  2. 0.9 0.6 0.9,  3. 1.0 0.4 1.0, 4. 0.9 0.0 1.0,  5. 0.7 0.0 1.0,  6. 0.5 0.0 0.8, 7. 0.0 0.0 0.8,  8. 0.0 0.0 1.0,  9. 0.0 0.6 1.0,10. 0.0 0.8 1.0, 11. 0.0 0.7 0.5, 12. 0.0 0.9 0.2,13. 0.5 1.0 0.0, 14. 0.8 1.0 0.0, 15. 1.0 1.0 0.0,16. 1.0 0.8 0.0, 17. 1.0 0.5 0.0, 18. 1.0 0.0 0.0,19. 0.8 0.0 0.0, 20. 0.6 0.0 0.0, 21. 0.0 0.0 0.0 )
set palette maxcolors 30
set logscale cb
set lmargin at screen 0.15

set rmargin at screen 0.75

splot 'gplevh.dat' us 1:2:3 notitle

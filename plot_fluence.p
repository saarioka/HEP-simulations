reset
set terminal png size 800,400
set output 'pics/'.title_str.'.png'
set title title_str
set grid front
set xlabel 'Energy [keV]'
set xtics
set ylabel 'Fluence [dn/dE]'
set ytics
set logscale x
set xrange [10:14E2]
set logscale y
set yrange [1:1E10]
unset logscale z
unset logscale cb
unset logscale x2
unset logscale y2

set key title "Beam energy"
set key outside
set key right

plot for [i=1:words(energies)] bulk_id.'_'.word(energies,i).'_'.file_id.'_tab.lis' ind 0 us (($1)*1000000.0):3 w histeps lt 1 lw 2 lc i notitle, \
NaN lt 1 lw 2 lc 1 title "30keV", \
NaN lt 1 lw 2 lc 2 title "60keV", \
NaN lt 1 lw 2 lc 3 title "478keV", \
NaN lt 1 lw 2 lc 4 title "661keV", \
NaN lt 1 lw 2 lc 5 title "1MeV", \
NaN lt 1 lw 2 lc 6 title "1.3MeV"

#for [i=start_index:24:4] 'versio1-'.i.'_22_tab.lis' ind 0 us ((sqrt($1*$2))*1000000.0):3:($3*$4/100.) w errorbars lt 1 lw 2 lc i/4 pt 0 ps 1 notitle, \


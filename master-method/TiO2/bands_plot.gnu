set datafile commentschars "&"
set term pngcairo size 1200,750
set output 'TiO2_bands.png'
set xlabel 'k-path'
set ylabel 'Energy (eV, VBM = 0)'
set grid ytics
set key off
set xtics ("{/Symbol G}" 0.0000, "X" 0.5000, "M" 1.0000, "{/Symbol G}" 1.7071, "Z" 2.4852, "R" 2.9852, "A" 3.4852, "Z" 4.1923)
set for [x in sprintf("%g %g %g %g %g %g %g %g", 0.0000,0.5000,1.0000,1.7071,2.4852,2.9852,3.4852,4.1923)]     arrow from x, graph 0 to x, graph 1 nohead lc rgb "#cccccc"
plot for [i=0:49] 'TiO2.bands.shifted.gnu' index i using 1:2 with lines lw 2

# Theobald Hose Stream

These data are taken from the following reference:

> C. Theobald. The effect of Nozzle Design on the Stability and Performance of Turbulent Water Jets.  Fire Safety Journal, 4(1981) 1-13.

The aim of this test series is to allow for hose stream applications in FDS.  This is accomplished by reducing the particle drag to near zero for particles within the jet stream, prior to "primary breakup".

The FDS cases use the "jet break-up length" reported in the paper as the PRIMARY_BREAKUP_LENGTH in the input files.

In the FDS repository, the python script `build_spray_input_files.py` reads `theobald_effect_1981_fds.csv` to generate the fds input files.

The file `Nozzle_10_shape_factor.csv` was digitized from Fig. 7 of the paper.  Data for the relative shape factors of the other nozzles is taken from Table 1 of the paper.
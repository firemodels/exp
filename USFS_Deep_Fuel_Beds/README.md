# USFS Deep Fuel Beds EXP PArameters

This directory contains experimental parameters, for  a python script in the fds repository to build fds input files.

## Mass Producing Input Files from a Template

The python script `build_input_files.py` reads `exp_params.csv`, wich contains the paramaters for the 108 experamental burns and converts them into paramaters to be inserted into `Template.fds`, making the file `paramfile.csv`. `build_input_files.py` then calls `swaps.py` from the fds Utilties directory, wich uses `Template.fds` and `paramfile.csv` to generate the fds input files and then moves these files up one level to FDS_Input_Files.

`build_input_files.py` is run from the fds repository, in `FDS_Input_Files/Build_Input_Files/`

# Askervein Hill EXP Files

This README documents the generation of EXP csv files for the Askervein Hill series.

The [Askervein 1983](https://drive.google.com/file/d/1gb21m8G6irryDDNEoKsXwXBETwlGnccK/view?usp=sharing) gives the relevant information.

All data is from run TU03-A

In general:
DZ= height off of ground
FSUP= Fractional speed up
uv, uw, vw = covariance

in the CSV data:
UPWASH = degrees upwash relative to the UV plane
AVGw = Mean vertical component
- in the report, UPWASH could mean either of these depending on the graph
DIRECTION = Wind direction in degrees, with North at 180 and East at 270

The data in the file ASW-ANE_TU03A_10m.csv is from Table A1.3 on page 70, and from DZ=10 on page78, and is plotted in Fig 4.3 on page 288(ledgend on page 278)
the Data is Described on page 66. (UPWASH = degrees upwash relative to the UV plane)
SIGM_SPEED was obtained, = (SIGMu.^2 +SIGMv.^2 +SIGMw.^2).^.5; for comparison with FDS 

The data in the file ASW60_TU03A_UK30m_tower.csv is from Table A1.4 on page 78, and described on page 74
SIGM_SPEED was obtained = (SIGMu.^2 +SIGMv.^2 +SIGMw.^2).^.5; for comparison with FDS 
"incd deg" in the data table is labeled UPWASH in the CSV file, as it refers to upwash angle relative to the u-v plane

The data in the files AASW-AANE_TU03A_10m.csv and BNW-BSE_TU03A_10m.csv are from the plots in Fig 3.3 on page 213, Extracted with http://www.graphreader.com/ (in 2021) 
DIST was then modifided to the known tower locations, and NORM_SPEED was multiplied by 10.5m/s (from page 213)to obtain the Mean Speed (SPEED) for comparison with FDS

The data in the files AASW-AANE_TU03A_10m_TU.csv, AASW-AANE_TU03A_10m_MF.csv, CP_TU03A_FRG17m_tower_MF.csv, and CP_TU03A_FRG17m_tower_TU.csv is
from Table A1.4 on page 87, and is plotted in Fig 4.4 on page 304(ledgend on page 298), and in Fig 4.2 on page 272(ledgend on page 266)
page 82 describes the data: DIF is 'hill wind directions minus refrence direction', FSUP is 'fractional speed up' and UPWSH is 'mean vertical component'(renamed to AVGw)
For AASW-AANE_TU03A_10m_TU.csv and CP_TU03A_FRG17m_tower_MF.csv SIGM_SPEED was obtained, SIGM_SPEEED = (SIGMu.^2 +SIGMv.^2 +SIGMw.^2).^.5; for comparison with FDS 
In the csv file UPWASH is in degrees relative to the UV plane, obtained UPWASH with UPWASH = atand(AVGw./(SPEED.^2 - AVGw.^2).^.5;);for comparison with FDS 
On page 87, the location AASW50 MF is mislabled as AASW40. The EXP File corrects this.

The data in the file RS-HT_TU03A_50m_tower.csv is from Table A1.7 on page 103, described on page 102, and plotted in Fig 4.1 on page 256(ledgend on page 246)


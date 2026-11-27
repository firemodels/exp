# BCL/VIB Hasenheide Apartment Experiments

Pool fires of a C7 hydrocarbon mixture traded as heptane in a vacant apartment in Leipzig, Germany,
conducted in December 2025. The apartment comprised the fire room F1, two further rooms F2 and F3, and a
corridor FC. Until the ventilation started, it exchanged air with its surroundings only through leakage.
14 runs in 3 fire series:

| Series | Pan width (mm) | Fuel mass (g) | Runs |
|---|---|---|---|
| Hep_160_075 | 160 | 75 | 7 |
| Hep_160_150 | 160 | 150 | 3 |
| Hep_220_300 | 220 | 300 | 4 |

## Source

- Osburg et al., "Measuring and modelling smoke light extinction in well-ventilated, multi-room compartment fires: Co-located transmissometry and a-priori FDS validation", Fire Safety Journal 167 (2027) 104997,
  https://doi.org/10.1016/j.firesaf.2026.104997
- Reproduction package openbcl/hasenheide1-reproduction v1.0.0 (commit 58cc1ea), https://doi.org/10.5281/zenodo.24054120,
  https://github.com/openbcl/hasenheide1-reproduction

The files in this folder are derived from the per-run time series of the package
(`results/measurement/timeseries`).

## Files

Each run has the files below. `<run>` is the run name of the package, e.g. `Hep_160_S2_R1` (pan width
160 mm, instrument setup S2). All files start at t = 0 and end at the start of the ventilation. Row 1 holds
the column names, row 2 the units, and the data start in row 3; the HGL files have one header row.

- `Hasenheide_<run>.csv`: transmissivity, `Trans_<room>_<z>` (%/m), and extinction coefficient,
  `K_<room>_<z>` (1/m), of the laser extinction meters (LEM, wavelength 638 nm, path length 0.81 m).
  `<room>` is F1, F2 or F3, `<z>` the height in m: `2_3` for the fixed LEM at 2.3 m in each room, and
  `1_5`, `1_9`, `2_1` for the movable LEM in F2.
- `Hasenheide_<run>_TC.csv`: thermocouple trees in F1 and F2, `TC_<room>_<z>` (°C), at 0.6, 1.2, 1.6, 1.8, 2.0, 2.2, 2.4, and 2.5 m.
- `Hasenheide_<run>_HGL_F1.csv`, `Hasenheide_<run>_HGL_F2.csv`: layer height and lower and upper layer
  temperature from the thermocouple tree, computed with `Utilities/Python/scripts/layer_height.py` of FDS
  (ceiling height 2.55 m).
- `Hasenheide_<run>_load_cell.csv`: fuel mass on the load cell as logged (pan tared, 1 s values), `Mass` (kg),
  and the heat release rate derived from it, `HRR` (kW).

## Processing

- **Time:** t = 0 is the ignition reference of the package; the logged ignition follows 0.5 s to
  2.8 s later.
- **Reference:** the LEM and thermocouple channels are referenced to their values at t = 0: K − K(0), and
  temperatures as the ambient temperature measured before the run plus T − T(0). The mass is not referenced.
- **Averaging:** the LEM and thermocouple data, and the HGL files computed from them, are averages over
  10 s intervals ending at the time given, as FDS writes device output every 10 s
  (`NFRAMES` = `T_END`/10 s), averaged over that interval.
  The row at t = 0 holds the reference. `Trans` is the interval mean of 100 exp(−K · 1 m), and
  `K` = −ln(`Trans`/100).
- **Rounding:** transmissivity 0.1 %/m, K 0.001 1/m, temperature 0.1 °C,
  height 0.01 m, mass 0.0001 kg, HRR 0.01 kW.
- **HRR** (Supplementary Material S5 of the paper, `scripts/reduce_hrr_from_mass.py` of the package):
  1. The mass is smoothed with a centred 15 s moving average.
  2. It is scaled linearly to equal the fuel charge at t = 0 and zero at flame-out.
  3. The mass loss rate is multiplied by the effective heat of combustion that FDS uses with
     `HEAT_OF_COMBUSTION` = 44.0 MJ/kg (net heat of combustion of the liquid fuel for
     complete combustion) and `IDEAL=T` for
     the soot and CO yields of the series:
     42.824 MJ/kg (Hep_160_075), 42.667 MJ/kg (Hep_160_150), 42.726 MJ/kg (Hep_220_300).
     The paper uses the measured effective heat of combustion, 41.345 MJ/kg.
  4. The result is smoothed with a trailing 21 s moving average and rescaled to the energy
     of the fuel charge. After flame-out, the HRR is zero.

  The HRR ramps of the FDS input files are these curves, thinned to 0.2 kW and rescaled to the fuel
  energy.

## Missing data

- No valid measurement: LEM `F1_2_3` in Hep_220_S1_R1, LEM `F1_2_3` in Hep_220_S1_R4.
- Thermocouple tree F2 below 2.0 m (separate logger) missing: Hep_160_S1_R3, Hep_160_S2_R1; these runs
  have no HGL file for F2.

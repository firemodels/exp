# Global convective heat transfer coefficients

Source: A. Bouchair, thesis, `Bouchair_THESIS_uk_bl_ethos_329792.pdf`,
Tables 4.29 and 4.30, printed page 104 (PDF page 113). The CSV transcribes
all 24 HTC values and their accompanying mass flow rates as printed.
HTC units are W/(m2 K). `mdot_exp_kg_s_m` is mass flow per unit cavity
span in kg/(s m). `mdot_exp_kg_s` is the total mass flow in kg/s, calculated
as `mdot_exp_kg_s_m * 1.5 m`.

The four columns correspond to wall temperatures 10, 20, 30, and 40 K above
20 C ambient, mapped here to FDS case temperatures 30, 40, 50, and 60 C.
See also Tables 4.25 and 4.26 (printed page 99) and Tables 4.33 and 4.34
(printed page 107). The mass flows are retained from the HTC tables:
Table 4.29 gives 0.095 for the 0.1 m inlet, 0.3 m gap, 50 C case, whereas
Table 4.25 gives 0.097; Table 4.30 gives 0.053 for the 0.4 m inlet, 0.3 m
gap, 30 C case, whereas Table 4.26 gives 0.060. No corrections are applied.

Equation 4.3, printed page 103 (PDF page 112), defines

    hc = M cp (T_out - T_in) / [2 Y Z (T_wall - T_bulk)]
    T_bulk = (T_in + T_out)/2

For total mass flow M in kg/s, use cavity span Y=1.5 m and height Z=2.0 m,
giving a nominal two-wall area of 6 m2. Equivalently, flow per unit span
uses area per unit span 2Z=4 m. The companion FDS script uses total `mdot`,
cp=1000 J/(kg K), T_in=20 C, and separate temporal means of `mdot` and
the spatially averaged `T_outlet` over the last half of the available run.
The area follows Eq. 4.3 without deducting the cavity inlet opening.

Bouchair excludes 0.5 and 1.0 m gaps from these HTC tables because of
flow complexity (printed page 103); no experimental HTC is assigned to them.

## Python comparison plot

`Utilities/Python/scripts/bouchair_htc.py` in the FDS repository writes
`Bouchair_HTC.csv` and `Bouchair_HTC.pdf`. The PDF plots positive matched
experimental/predicted HTC pairs on equal log scales. Black lines show
unity and experimental spread; red lines show model bias and model spread.
The statistics use the ten-bin weighting and log-ratio formulas from
`fdsplotlib.scatplot`. Dashed bounds use factors `1+2*sigma`, as in FDS.

Supply `--sigma-e` as a relative standard deviation (fraction) when an HTC
experimental uncertainty is available. If omitted, the FDS fallback sets
experimental and model variances equal to half the log-ratio variance;
the PDF explicitly labels the experimental uncertainty as estimated.
This fallback is not a thesis-reported uncertainty. The 0.08 mass-flow
uncertainty from the reference figure is not assigned to HTC.

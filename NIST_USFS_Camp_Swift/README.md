Data from the Camp Swift Fire Experiments can be found via [this storymap](https://usfs.maps.arcgis.com/apps/MapJournal/index.html?appid=aa3726577d9549a2a26b7d000fb98512) or from the [USFS Research Data Archive](https://www.fs.usda.gov/rds/archive).

**Fire Behavior Packages:**

Fire Behavior Packages (FBPs) provided in-situ measurement of heat flux and temperature. The full data are available [here](https://www.fs.usda.gov/rds/archive/catalog/RDS-2018-0042), while a simplified version with variables used for comparison to FDS has been created with the `./data_processing/parse_FBP_data.py` script. The 'time' column for each file is adjusted to match the experimental ignition time with the activation of the ignition `VENT` in FDS.

The following table provides a reference for the location of each sensor using the EPSG 26914 coordinate reference system:
| FBP ID   | Burn block   |     x (m) |      y (m) |
|:---------|:-------------|----------:|-----------:|
| 6C       | BB1          | 666328.35 | 3347260.83 |
| 13E      | BB1          | 666361.57 | 3347265.74 |
| 15W      | BB1          | 666299.91 | 3347252.81 |
| 17S      | BB1          | 666345.56 | 3347237.52 |
| 9N       | BB1          | 666318.67 | 3347290.30 |
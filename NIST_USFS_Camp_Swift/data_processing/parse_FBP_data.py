### This script parses the Fire Behavior Package geodatabase and cleans it up
### for archiving in the firemodels/exp repo.
### Database located at https://www.fs.usda.gov/rds/archive/catalog/RDS-2018-0042

import geopandas as gpd
import pandas as pd
import numpy as np
from datetime import datetime

# initialize metadata table
meta = pd.DataFrame(columns=['FBP ID', 'Burn block', 'x (m)', 'y (m)'])

# FDS ignition times in UTC (based on ignition line activation relative to T_BEGIN)
ig_time={'BB1':'18:32:05.0',
         'BB2':'19:43:21.0',
         'BB3':'21:01:35.0'}
fds_t_offset={'BB1':9}
    
# Read the GDB into a GeoDataFrame (assumes it has been downloaded - update path as necessary)
gdf = gpd.read_file(r"FireBehaviorPackage.gdb")

# Columns to keep for firemodels/exp
keep_columns=['UTCTime','Temperature_C','MT_rad_kW_m_2','NAR_kW_m_2']

sensor_IDs = gdf['ID'].unique()

for sensor in sensor_IDs:
    out = gdf[gdf['ID']==sensor]
    
    x_coord = out.get_coordinates()['x'].values[0]
    y_coord = out.get_coordinates()['y'].values[0]
    
    if (y_coord<3347330):
        BB_ID='BB1'
    elif (y_coord<3347450):
        BB_ID='BB2'
    else:
        BB_ID='BB3'
    
    # strip data for repo
    out=out[keep_columns]
    out.iloc[:,1:4]=out.iloc[:,1:4].round(2)
    
    # for now only process BB1
    if BB_ID=='BB1':
        # find "FDS time" of first row
        t_row_0 = datetime.strptime(out['UTCTime'].values[0],'%H:%M:%S.%f').timestamp()
        t_ig_fds = datetime.strptime(ig_time[BB_ID],'%H:%M:%S.%f').timestamp()-fds_t_offset[BB_ID]
        
        t_fds = np.round(t_row_0 - t_ig_fds + np.arange(0, len(out)) * 0.1,1)
        out.insert(0,'time',t_fds)
        
        out.to_csv(sensor+'FBP.csv',index=False)
        
        # append metadata
        meta.loc[len(meta)]=[sensor,BB_ID,x_coord,y_coord]
        
# write out metadata
print(meta.to_markdown(index=False,floatfmt=".2f"))
        

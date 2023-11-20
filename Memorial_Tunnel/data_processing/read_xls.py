"""read_xls
This script opens the original Memorial Tunnel Excel (.XLS) files and converts the "Graph Data" to comma-delimited (.csv) files
"""

import csv
import xlrd
import numpy as np
import pandas as pd

df = pd.read_csv("File_Names.csv",header=0)

for name_row in df.index:
    original_file     = str(df.loc[name_row,"Original File"])
    print(original_file)
    converted_file    = str(df.loc[name_row,"Converted File"])
    conversion_factor = float(df.loc[name_row,"Conversion Factor"])
    conversion_addend = float(df.loc[name_row,"Conversion Addend"])
    units             = str(df.loc[name_row,"Units"])
    book = xlrd.open_workbook(original_file)
    sh = book.sheet_by_name("Graph_Data")
    
    with open(converted_file,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,dialect='unix')
        csvwriter.writerow(sh.row_values(4,start_colx=2,end_colx=sh.ncols))
        time_list = ['s']
        unit_list = [units for j in range(sh.ncols-3)]
        csvwriter.writerow(np.concatenate((time_list,unit_list),axis=0))
        for row in range(6,sh.nrows,1): 
            t =   np.array([float(f) for f in sh.row_values(row,start_colx=2,end_colx=3)])
            dat = np.array([float(f) for f in sh.row_values(row,start_colx=3,end_colx=sh.ncols)])
            con = dat*conversion_factor + conversion_addend
            output = np.concatenate((t,con),axis=0)
            if sh.row_values(row)[2]>0.5 or sh.row_values(row+1)[2]>0.5:
               csvwriter.writerow("%.2f"%f for f in output)


# Noelle Crump 7/7/2022
# reads XLS Memorial Tunnel document data into csv files

import pandas as pd
from os import listdir

# Read in Data:
sheet_index = 1                                           # sheet number index (set to sheet 2)
n_headers = 2                                             # number of header rows
key_list = ['ELAPSED_TIME',' ELAPSED_TIME','ELAPSED']     # top left corner of relevant data in exell sheets
file_list = [f for f in listdir() if f[-4:] == '.XLS']    # reads in all .XLS files in current folder

for filename in file_list:                                # for all .XLS files within current folder
	nf = filename.replace('.XLS','.csv')                  # change output file extension
	nf = nf.replace('QP','VF')                            # renames QP files VF
	len_fk = 2                                            # adds '-' to new filename
	if filename[:3] == 'HRR':
		len_fk = 3
	new_filename = nf[:len_fk] +'-'+ nf[len_fk:len(nf)]

	# - reads sheet, finds target data, re-reads in relevent data -
	key_index = []
	header_index = []
	df = pd.read_excel(filename, sheet_name=sheet_index)
	for row in df.index:
		for col in df.columns:
			for key in key_list:
				if (key == df.loc[row,col]) and (len(key_index) == 0):
					key_index = [row+1,df.columns.get_loc(col)]
	for n in range(n_headers):
		header_index = header_index + [key_index[0]+n]
	df = pd.read_excel(filename, sheet_name=sheet_index, header=header_index,index_col=key_index[1])

# Pre-Cleaning:
	# - removes spaces & multiindex, stores units, makes time column, fixes typo -
	df = df.dropna(axis=1)                                # removes empty columns
	df_columns = []
	df_units = []
	for name in df.columns:                               # removes spaces in strings
		df_columns = df_columns + [name[0].replace(' ','')]
		df_units = df_units + [name[1].replace(' ','')]

	for num in range(len(df_columns)):                    # typo fix
		if (df_columns[num] == 'VT305A2V'):
			df_units[num] = 'FPM'
			if (df_columns[num + 1] == 'VT307B2V'):
				df_columns[num] = 'VT307A2V'
	df_columns[0] = 'Time'                                # fixes Time column in VF_files

	df.columns = df_columns                               # new Index and Time column
	df_Time = df.index
	df.index = (range(len(df_Time)))
	df['Time'] = df_Time

# Conversions:
	# - converts data given unit in. returns data and units as tupple -
	def convert(input_value,input_unit):
		if input_unit == 'F':
			value_out = int(round((input_value-32.0)*(5.0/9.0),0))
			unit_out = 'C'
		elif input_unit == 'FPM':
			value_out = round((input_value/196.8504),2)
			unit_out = 'm/s'
		elif input_unit == 'CFM':
			value_out = round((input_value/2118.644),1)
			unit_out = 'm3/s'
		elif input_unit == 'MW':
			value_out = int(round((input_value/1000),0))
			unit_out = 'kW'
		elif input_unit == 'PPM':
			value_out = round((input_value/1e6),6)
			unit_out = 'mol/mol'
		elif input_unit == 'round_1':
			value_out = round(input_value,1)
			unit_out = input_unit
		elif input_unit == '':
			value_out = input_value
			unit_out = input_unit
		else:
			print ("conversion type not supported (yet?)")
			return(input_value, input_unit)
		return[value_out,unit_out]

	# - sets what columns need which conversions. works for either headers or units -
	def col_unit(col_in):
		if(col_in == 'QI001'):
			return('MW')
		elif(col_in == 'Loop'):
			return('CFM')
		elif(col_in == 'Time'):
			return('round_1')
		else:
			return(col_in)

	# - perform conversions: search for specific headers to convert their data -
	col_keys = ['Time','F','QI001','FPM','Loop','PPM']

	data_out = []                                         # initalize outgoing matrix
	for row in df.index:
		new_row = []
		for col_n in range (len(df.columns)):
			for key in col_keys:                          # check each key for correct conversion
				if key == df_columns[col_n] or key == df_units[col_n]:
					value = df.iloc[row,col_n]
					new_row = new_row + [convert(value,col_unit(key))[0]]
					this_key = key                        # sets key for df_units  conversion
		data_out = data_out + [new_row]                   # adds new row to outgoing matrix

# Post Cleaning:
    # - rename column headers -
	for col_n in range(len(df_columns)):
		head = df_columns[col_n]
		if head == 'QI001':
			df_columns[col_n] = 'HRR'
		if head[:4] == 'Loop':
			df_columns[col_n] = df_units[col_n] + '-VF'
		if head[:2] == 'VT':
			df_columns[col_n] = head[2:5] + '-U-' + head[5:7]
		if head[:2] == 'TI':
			df_columns[col_n] = head[4:7] + '-T-' + head[7] + '2'
		if head[:2] =='CT':
			df_columns[col_n] = head[2:5] + '-CO-' + head[-2:]

	#  - converts units row -
	this_key =  convert(value,col_unit(this_key))[1]
	df_units = []
	for f in range(len(df_columns)):
		df_units = df_units + [this_key]
	df_units[0] = 's'

# Exporting:
	# - put it all together -
	dfoutdata = pd.DataFrame(data_out)                   # build dfout dataframe
	dfoutunits = pd.DataFrame(df_units)
	dfout = pd.concat([dfoutunits.transpose(),dfoutdata])
	dfout.columns = df_columns

	dfout = dfout.dropna(axis=1)                         # Drops empty columns
	dfout = dfout.drop_duplicates()                      # Drops duplicate rows
	dfout.index = (range(len(dfout)))                    # reorders index after drop

	df_Time = dfout['Time']                              
	dfout = dfout.drop(index=(len(df_Time)-1))           # removes last row of data 
	for n in range (1,6):                                # removes leading zeroes
		if (df_Time[n] == 0) and (df_Time[n+1] == 0):
			dfout = dfout.drop(index=n)

	print('writing file ' + new_filename)
	dfout.to_csv(new_filename, index=False)              # write final csv file

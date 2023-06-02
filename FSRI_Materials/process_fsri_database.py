import os
import glob
import numpy as np
import pandas as pd
import shutil
import matplotlib.pyplot as plt
# This script will import data from the FSRI material database and evaluate
# the scaling pyrolysis model on all materials.
# To use this script, clone the FSRI database into the same root directory
# as fds, exp, and out
#
# git clone git@github.com:ulfsri/fsri_materials_database.git
# 
# Then navigate to the scripts directory and run collect_thermophysical_properties.py
#
# cd fsri_materials_database/02_Scripts/Utilities/
# python collect_thermophysical_properties.py
#
# Then run this script.

def extractConeAnalysisData(values, scaled_times, tigns, uniqueFluxes):
    coneAnalysisData = dict()
    for i, flux in enumerate(uniqueFluxes):
        
        v = values[i]
        t = scaled_times[i]
        tign = tigns[i]
        coneAnalysisData[flux] = dict()
        coneAnalysisData[flux]['peakHRRPUA'] = np.max(v)
        coneAnalysisData[flux]['timeToPeak'] = t[np.argmax(v)]-tign
        
        tMax = int(np.ceil(t.max()))
        tMax = max([tMax, 60])
        t2 = np.linspace(0, tMax, tMax+1)
        v2 = np.interp(t2, t, v)
        
        dt = t2[1] - t2[0]
        
        filters = [int(60/dt), int(180/dt), int(300/dt)]
        filteredValues = []
        for f in filters:
            fil = np.ones(f)/float(f)
            vfilt = np.convolve(v2, fil, mode='same')
            filteredValues.append(np.max(vfilt))
        
        coneAnalysisData[flux]['avg60s'] = filteredValues[0]
        coneAnalysisData[flux]['avg180s'] = filteredValues[1]
        coneAnalysisData[flux]['avg300s'] = filteredValues[2]
    return coneAnalysisData

def air_density(temperature):
    # returns density in kg/m3 given a temperature in C
    rho = 1.2883 - 4.327e-3*temperature + 8.78e-6*temperature**2
    return rho

def getConeData(material, directory, e=13100):
    p = os.path.abspath(directory+os.sep+'Cone')
    files = glob.glob(p+os.sep+'*Cone_H*.csv')
    files = [x for x in files if "Scalar" not in x]
    
    try:
        tmp_prop = pd.read_csv(p+os.sep + material+'_Ignition_Temp_Properties.csv', header=None, index_col=0).T
        density = tmp_prop['Density (kg/m3)'].values[0]
    except:
        density = False
    
    # Hard coded fixes for consistency, see notes for each
    if material == "HDPE":
        files = [x for x in files if (('_R4' not in x) and ('_R5' not in x) and ('_R6' not in x))]
        # _R5 and _R6 used a 60 mm spacing which differed from _R1 through _R4
        # _R4 warped and contacted spark ignitor leadi nto differenet burning behavior
    if material == 'EPDM_Membrane':
        files2 = []
        for file in files:
            if 'HF25' in file and (('_R3' in file) or ('_R4' in file) or ('_R5' in file)):
                files2.append(file)
            if (('HF50' in file) or ('HF75' in file)) and ('_R4' not in file):
                files2.append(file)
        files = files2
    if material == 'Nylon':
        files = [x for x in files if (('_R4' not in x) or ('HF25' not in x))]
        # _R4 used retaining frame
    if material == 'PET':
        files = [x for x in files if (('_R4' not in x) or ('HF25' not in x))]
        files = [x for x in files if (('_R5' not in x) or ('HF25' not in x))]
        # _R4 and _R5 used 60 mm spacing
    if material == 'Polyisocyanurate_Foam_Board':
        files = [x for x in files if ('_R1' not in x)]
        # _R1 left foil on the sample whereas R2-R4 removed
    if material == 'Vinyl_Tile':
        files = [x for x in files if ('_R4' not in x)]
        # _R4 different test conditions than R1-R3
    coneData = dict()
    for j, file in enumerate(files):
        dc = pd.read_csv(file, skiprows= [1,2,3,4], index_col='Names', header=0)
        rev = file.split('_')[-1].split('.csv')[0]
        HF = file.split('HF')[1].split('Scalar')[0].split('_')[0].replace('Scan','')
        f = '*' + '_Cone_HF' + HF + 'Scalar_*_' + rev + '.csv'
        d = glob.glob(os.path.join(p, f))[0]
        ds = pd.read_csv(d, header=None, index_col=0).squeeze()
        # Data modification from pre-test notes and HRR calculation
        # copied from FSRI processing scripts
        try:
            pretest_notes = ds.at['PRE TEST CMT']
        except:
            pretest_notes = ' '
        surf_area_mm2 = 10000
        dims = 'not specified' 
        frame = False
        thickness = False
        for notes in pretest_notes.split(';'):
            if 'Dimensions' in notes:
                tmp = notes.split('Dimensions:')[1].split(' ')
                dims = []
                for i in tmp:
                    try:
                        dims.append(float(i))
                    except: continue
                surf_area_mm2 = dims[0] * dims[1]
                thickness = dims[2]
            elif 'frame' in notes: 
                frame = True
        if frame or '-Frame' in f:
            surf_area_mm2 = 8836
        surf_area_m2 = surf_area_mm2 / 1000000.0
        mass = float(ds.at['SPECIMEN MASS']) / 1000
        c_factor = float(ds.at['C FACTOR'])
        dc['O2 Meter'] = dc['O2 Meter']/100
        dc['CO2 Meter'] = dc['CO2 Meter']/100
        dc['CO Meter'] = dc['CO Meter']/100
        
        dc.loc[:,'EDF'] = ((dc.loc[:,'Exh Press']/(dc.loc[:,'Stack TC']+273.15)).apply(np.sqrt)).multiply(c_factor) # Exhaust Duct Flow (m_e_dot)
        dc.loc[:,'Volumetric Flow'] = dc.loc[:,'EDF']*air_density(dc.loc[:,'Smoke TC']) # Exhaust Duct Flow (m_e_dot)
        dc.loc[:,'ODF'] = (dc.at['Baseline', 'O2 Meter'] - dc.loc[:,'O2 Meter']) / (1.105 - (1.5*(dc.loc[:,'O2 Meter']))) # Oxygen depletion factor with only O2
        dc.loc[:,'ODF_ext'] = (dc.at['Baseline', 'O2 Meter']*(1-dc.loc[:, 'CO2 Meter'] - dc.loc[:, 'CO Meter']) - dc.loc[:, 'O2 Meter']*(1-dc.at['Baseline', 'CO2 Meter']))/(dc.at['Baseline', 'O2 Meter']*(1-dc.loc[:, 'CO2 Meter']-dc.loc[:, 'CO Meter']-dc.loc[:, 'O2 Meter'])) # Oxygen Depletion Factor with O2, CO, and CO2
        dc.loc[:,'HRR'] = 1.10*(e)*dc.loc[:,'EDF']*dc.loc[:,'ODF']
        dc.loc[:,'HRR_ext'] = 1.10*(e)*dc.loc[:,'EDF']*dc.at['Baseline', 'O2 Meter']*((dc.loc[:,'ODF_ext']-0.172*(1-dc.loc[:,'ODF'])*(dc.loc[:, 'CO2 Meter']/dc.loc[:, 'O2 Meter']))/((1-dc.loc[:,'ODF'])+1.105*dc.loc[:,'ODF']))
        dc.loc[:,'HRRPUA'] = dc.loc[:,'HRR']/surf_area_m2
        
        if density is False and thickness is False:
            print(material, "Failed to get density assuming 1 inch")
            thickness = 0.0254
            density =  mass / (thickness * surf_area_m2)
        elif density is False:
            density =  mass / (thickness/1000 * surf_area_m2)
            thickness = thickness / 1000
        elif thickness is False:
            thickness = mass / (density*surf_area_m2)
        else:
            thickness = thickness/1000
        
        coneData[j] = dict()
        coneData[j]['flux'] = float(ds.at['HEAT FLUX']) # kW/m2
        coneData[j]['mass'] = mass # kg
        coneData[j]['area'] = surf_area_m2
        coneData[j]['thickness'] = thickness
        coneData[j]['density'] = density
        coneData[j]['time'] = dc['Time']
        coneData[j]['hrrpua'] = dc['HRRPUA']
        coneData[j]['timeMax'] = np.nanmax(dc['Time'])
        coneData[j]['timeInt'] = float(ds.at['SCAN TIME'])
        coneData[j]['timeIgn'] = float(ds.at['TIME TO IGN']) # m2
        try:
            HF_float = float(HF)
        except:
            HF_float = float(HF.split('-')[0])
        if HF_float != float(ds.at['HEAT FLUX']):
            print(file, float(ds.at['HEAT FLUX']))
    
    coneData = pd.DataFrame(coneData).T
    
    return coneData

def importFsriMaterial(p, material, outInt, filterWidth=101, dt=0.1):
    material_dict = dict()
    coneData = getConeData(material, p)
    ignitionFname = p+os.sep+'Cone' + os.sep + material+'_Ignition_Temp_Properties.csv'
    if os.path.exists(ignitionFname) is False:
        density = np.mean(coneData['density'].values)
        conductivity = 0.2
        heatCapacity = 1.
    else:
        tmp_prop = pd.read_csv(ignitionFname, header=None, index_col=0).T
        conductivity = tmp_prop['Thermal Conductivity (W/m-K)'].values[0]
        heatCapacity = tmp_prop['Heat Capacity (J/kg-K)'].values[0]/1000.
        density = tmp_prop['Density (kg/m3)'].values[0]

    
    material_dict['conductivity'] = conductivity
    material_dict['heatCapacity'] = heatCapacity
    material_dict['density'] = density
    material_dict['directory'] = p
    
    
    thicknesses = []
    fil1 = np.ones(filterWidth)/filterWidth
    
    for flux in np.unique(coneData['flux'].values):
        outInt2 = outInt
        #dt = np.min(coneData.loc[coneData['flux'] == flux, 'timeInt'].values)
        tMax = np.max(coneData.loc[coneData['flux'] == flux, 'timeMax'].values)
        
        thickness = np.median(coneData.loc[coneData['flux'] == flux, 'thickness'].values)
        mass = np.median(coneData.loc[coneData['flux'] == flux, 'mass'].values)
        area = np.median(coneData.loc[coneData['flux'] == flux, 'area'].values)
        tign = np.median(coneData.loc[coneData['flux'] == flux, 'timeIgn'].values)
        
        times = coneData.loc[coneData['flux'] == flux, 'time'].values
        hrrpuas = coneData.loc[coneData['flux'] == flux, 'hrrpua'].values
        
        # Interpolate and filter raw data
        time = np.linspace(0, tMax, int(tMax/dt)+1)
        hrrpua = np.zeros_like(time)
        hrrpuas_interp = np.zeros((time.shape[0], len(times)))
        hrrpuas_interp_filtered = hrrpuas_interp.copy()
        
        for j in range(0, len(times)):
            h = np.interp(time, times[j], hrrpuas[j], right=np.nan)
            h[h < 0] = 0
            hrrpuas_interp[:, j] = h 
            hrrpuas_interp_filtered[:, j] = np.convolve(h, fil1, mode='same')
            #hrrpuas_interp[:, j] = np.convolve(h, fil, mode='same')
        
        # Find time to ignitions
        tIgns = []
        energyThreshold = 0.01
        truncateTime = False
        truncateBelow = False
        truncateBelow = 10
        # Hardcoded fixes for specific materials
        if material == 'Luan_Panel':
            energyThreshold = 0.005
        if material == 'Overstuffed_Chair_Polyester_Batting':
            if flux == 75:
                energyThreshold = 0.02
            elif flux == 50:
                energyThreshold = 0.03
            elif flux == 25:
                energyThreshold = 0.03
                truncateBelow = 50
        if material == 'Lightweight_Gypsum_Wallboard':
            if flux == 25:
                energyThreshold = 0.05
        if material == 'MDF':
            if flux == 50:
                truncateTime = 1000
        if material == 'Nylon_Carpet_High_Pile':
            if flux == 25:
                energyThreshold = 0.08
        if material == 'PETG':
            if flux == 25:
                energyThreshold = 0.02
        if material == 'Pine_Siding':
            if flux == 75:
                truncateTime = 700
        if material == 'PlasticB':
            if flux == 25:
                energyThreshold = 0.011
            else:
                energyThreshold = 0.001
        if material == 'Plastic_Laminate_Countertop':
            if flux == 25:
                energyThreshold = 0.02
        if material == 'Polyester_Bed_Skirt':
            if flux == 25:
                energyThreshold = 0.02
                truncateBelow = 10
        if material == 'Polyester_Microfiber_Sheet':
            if flux == 25:
                truncateBelow = 10
        if material == 'PVC':
            if flux == 25:
                truncateBelow = 20
        if material == 'Roof_Felt':
            if flux == 25:
                truncateBelow = 20
        if material == 'Vinyl_Siding':
            if flux == 25:
                truncateBelow = 20
        
        if truncateTime is not False:
            hrrpuas_interp[time > truncateTime, :] = 0
            hrrpuas_interp_filtered[time > truncateTime, :] = 0
        if truncateBelow is not False:
            hrrpuas_interp[hrrpuas_interp_filtered < truncateBelow] = 0
            hrrpuas_interp_filtered[hrrpuas_interp_filtered < truncateBelow] = 0
        for j in range(0, len(times)):
            inds = np.where(~np.isnan(hrrpuas_interp_filtered[:, j]))
            totalEnergy = np.trapz(hrrpuas_interp_filtered[inds, j], time[inds])
            #totalEnergy = np.trapz(hrrpuas_interp[:, j], time)
            totalEnergy2 = 0
            ind2 = 1
            while totalEnergy2 < energyThreshold * totalEnergy:
                ind2 = ind2 + 1
                totalEnergy2 = np.trapz(hrrpuas_interp_filtered[:ind2, j], time[:ind2])
            #hrrpuas_interp[:, j] = np.interp(time-time[ind2-1], time, hrrpuas_interp[:, j])
            if material == 'Gypsum_Wallboard':
                pass
                #print(totalEnergy2, energyThreshold, totalEnergy)
                #print(hrrpuas_interp[:, j])
            tIgns.append(time[ind2-1])
        tign = np.median(tIgns)
        
        # Average neglecting time to ignition
        hrrpuas_interp_notign = np.zeros_like(hrrpuas_interp)
        for j in range(0, len(times)):
            hrrpuas_interp_notign[:, j] = np.interp(time, time-tIgns[j], hrrpuas_interp[:, j], right=np.nan)
            if material == 'Vinyl_Tile' and flux == 25:
                pass
                plt.plot(time, hrrpuas_interp_notign[:, j])
                #plt.xlim(0, 400)
        
        #hrrpuas_interp_notign[np.isnan(hrrpuas_interp_notign)] = 0.0

        hrrpua = np.nanmean(hrrpuas_interp_notign, axis=1)        
        hrrpua_std = np.nanstd(hrrpuas_interp_notign, axis=1)
        hrrpua_mn = np.nanmin(hrrpuas_interp_notign, axis=1)
        hrrpua_mx = np.nanmax(hrrpuas_interp_notign, axis=1)
        
        tMax = time.max()
        
        filterWidth2 = int(min([max([filterWidth/600 * tMax, 31]), filterWidth]))
        fil2 = np.ones(filterWidth2)/float(filterWidth2)
        
        hrrpua = np.convolve(hrrpua, fil2, mode='same')
        
        hrrpua_for_energy = hrrpua.copy()
        hrrpua_for_energy[np.isnan(hrrpua_for_energy)] = 0
        
        
        tMax = np.ceil((tMax)/outInt2)*outInt2
        outTime = np.linspace(0, tMax, int(tMax/outInt2)+1)
        outHrrpua = np.interp(outTime, time, hrrpua_for_energy)
        
        totalEnergy = np.trapz(hrrpua_for_energy, time)
        totalEnergy2 = np.trapz(outHrrpua, outTime)
        
        peakHrrpua2 = np.nanmax(outHrrpua)
        peakHrrpua = np.nanmax(hrrpua)
        
        while abs(totalEnergy2 - totalEnergy)/totalEnergy > 0.001 or abs(peakHrrpua2 - peakHrrpua)/peakHrrpua > 0.01:
            outInt2 = outInt2*0.9
            outTime = np.linspace(0, tMax, int(tMax/outInt2)+1)
            outHrrpua = np.interp(outTime, time, hrrpua_for_energy)
            totalEnergy2 = np.trapz(outHrrpua, outTime)
            peakHrrpua2 = np.nanmax(outHrrpua)
            if outInt2 <= 0.1:
                totalEnergy2 = totalEnergy
        
        if tign > 0:
            outTime = np.append(np.array([0, tign*0.98]), outTime+tign)
            outHrrpua = np.append(np.array([0, 0]), outHrrpua)
        
        outHrrpua[outHrrpua < 0] = 0
        
        #if material == 'High_Temperature_SCBA_Facepiece':
        if material == 'Vinyl_Tile':
            print(flux, tign*0.98)
            print(flux, tIgns)
            print(flux, outInt2, totalEnergy, totalEnergy2, peakHrrpua, peakHrrpua2)
            plt.plot(outTime, outHrrpua)
            plt.xlim(0, 400)
            #assert False, "Stopped"
            pass
        
        material_dict[flux] = dict()
        material_dict[flux]['time'] = outTime
        material_dict[flux]['hrrpua'] = outHrrpua
        material_dict[flux]['hrrpua_full_mean'] = hrrpua
        material_dict[flux]['hrrpua_full_std'] = hrrpua_std
        material_dict[flux]['time_full'] = time
        material_dict[flux]['tIgn'] = tign
        material_dict[flux]['thickness'] = thickness
        material_dict[flux]['hrrpuas_interp'] = hrrpuas_interp
        material_dict[flux]['hrrpuas_interp_notign'] = hrrpuas_interp_notign
        material_dict[flux]['time_interp'] = time
        material_dict[flux]['hrrpua_full_min'] = hrrpua_mn
        material_dict[flux]['hrrpua_full_max'] = hrrpua_mx
        thicknesses.append(thickness)
    material_dict['thickness'] = np.median(thicknesses)
    
    return material_dict

def checkMaterial(p, material, ignores):
    if material in ignores: return False
    files = glob.glob(p+os.sep+'Cone'+os.sep+'*Cone_H*')
    if len(files) == 0: return False
    if os.path.exists(p+os.sep+'Cone' + os.sep + material+'_Ignition_Temp_Properties.csv') is False:
        print("Warning material %s does not have ignition temp properties"%(material)) 
        #complete = False
    return True

def importFsriDatabase(data_dir, outInt, Tinfty=300,
                       ignores=['Cotton_Sheet','Face_Shield','Overstuffed_Chair_Polyester_Fabric',
                                'Fiberglass_Insulation_R13_Paper_Faced',
                                'Fiberglass_Insulation_R30',
                                'Fiberglass_Insulation_R30_Paper_Faced',
                                'Hemp_Sheet',
                                'House_Wrap',
                                'Mineral_Wool_Insulation',
                                'Window_Screen']):
    material_directories = glob.glob(os.path.join(os.path.abspath(data_dir),'*'))
    possible_materials = [d.split(os.sep)[-1] for d in material_directories]
    
    complete_materials = dict()
    materials = []
    for i in range(0, len(material_directories)):
        p = os.path.abspath(material_directories[i])
        check = checkMaterial(p, possible_materials[i], ignores)
        if check: materials.append(possible_materials[i])
    for i in range(0, len(materials)):
        material = materials[i]
        p = os.path.join(os.path.abspath(data_dir), material)
        if True: #material == 'Vinyl_Tile':
            material_dict = importFsriMaterial(p, material, outInt)
            complete_materials[material] = material_dict
        
    return complete_materials

def interpolateExperimentalData(times, HRRs, targetDt=False, filterWidth=False):
    dt = np.nanmedian(times[1:]-times[:-1])
    if filterWidth is not False:
        filterWidth = int(filterWidth/dt)
        fil = np.ones(filterWidth)/filterWidth
        HRRs = np.convolve(HRRs, fil, mode='same')
    
    if targetDt is not False:
        dt = targetDt
    else:
        dt = np.nanmedian(times[1:]-times[:-1])
    tmax = np.round(times.max()/dt)*dt
    tmin = np.round(times.min()/dt)*dt
    targetTimes = np.linspace(tmin, tmax, int((tmax-tmin)/dt + 1))
    HRRs = np.interp(targetTimes, times, HRRs)
    
    return targetTimes, HRRs


if __name__ == "__main__":
    
    raw_data_dir = '../../fsri_materials_database/01_Data/'
    out_dir = '../../exp/FSRI_Materials/'
    
    material_directories = glob.glob(raw_data_dir+'*')
    possible_materials = [d.split(os.sep)[-1] for d in material_directories]
    
    out_dir = os.path.abspath(out_dir)
    if os.path.exists(out_dir) is False: os.mkdir(out_dir)
    raw_data_dir = os.path.abspath(raw_data_dir)
    
    material_database = importFsriDatabase(raw_data_dir, 15)
    
    resultDir = "../../../out/Scaling_Pyrolysis/"
    inputFileDir = "../../../fds/Validation/Scaling_Pyrolysis/"
    expFileDir = "../../../exp/FSRI_Materials/"
    emissivity = 1
    txt = 'Code,Number,Material,DataFile,ResultDir,InputFileDir,ExpFileDir,'
    txt = txt + 'ReferenceExposure,ReferenceTime,ReferenceHRRPUA,'
    txt = txt + 'ValidationTimes,ValidationHrrpuaColumns,ValidationFluxes,'
    txt = txt + 'Density,Conductivity,SpecificHeat,Emissivity,Thickness,'
    txt = txt + 'IgnitionTemperature,IgnitionTemperatureBasis,HeaderRows,FYI'

    for material in list(material_database.keys()):
        conductivity = material_database[material]['conductivity']
        specific_heat = material_database[material]['heatCapacity']
        density = material_database[material]['density']
        thickness = material_database[material]['thickness']
        
        fluxes = [x for x in list(material_database[material].keys()) if type(x) is float]
        fluxes.sort()
        
        code ='d'
        number = 1
        mat = 'FSRI_%s'%(material)
        dataFiles = ''
        for flux in fluxes:
            dataFile = os.path.join(expFileDir, '%s-%02d.csv'%(mat, flux))
            dataFiles = dataFiles + dataFile + '|'
        dataFiles = dataFiles[:-1]
        

        if (50 in fluxes):
            refFlux = 50
        else:
            ind = np.argmin([abs(x-50) for x in fluxes])
            refFlux = fluxes[ind]
        
        txt = txt + "\n" + "%s,%s,%s,%s,%s,"%(code, number, mat, dataFiles, resultDir)
        txt = txt + "%s,%s,%0.0f,%s-%0.0f.csv-Time,%s-%0.0f.csv-HRRPUA,"%(inputFileDir, expFileDir, refFlux, mat, refFlux, mat, refFlux)
        
        for flux in fluxes:
            txt = txt + '%s-%0.0f.csv-Time|'%(mat, flux)
        txt = txt[:-1] + ','
        for flux in fluxes:
            txt = txt + '%s-%0.0f.csv-HRRPUA|'%(mat, flux)
        txt = txt[:-1] + ','
        for flux in fluxes:
            txt = txt + '%0.0f|'%(flux)
        txt = txt[:-1] + ','
        txt = txt + '%0.1f,%0.4f,%0.4f,%0.4f,%0.8f,'%(density, conductivity, specific_heat, emissivity, thickness)
        txt = txt + 'Calculate,'
        for flux in fluxes:
            txt = txt + '%0.0f|'%(flux)
        txt = txt[:-1] + ','
        for flux in fluxes:
            txt = txt + '1|'
        txt = txt[:-1] + ','
        txt = txt + 'FSRI_materials'
        
        
        

        
        for flux in fluxes:
            tign = material_database[material][flux]['tIgn']
            
            times = material_database[material][flux]['time']
            hrrpuas = material_database[material][flux]['hrrpua']
            
            d = pd.DataFrame(np.array([times, hrrpuas]).T, columns=['Time','HRRPUA'])
            dataFile = os.path.abspath(os.path.join(out_dir,'%s-%02d.csv'%(mat, flux)))
            d['HRRPUA'] = d['HRRPUA'].round(decimals=1)
            d.to_csv(dataFile, index=False)
            
    with open('fsri_spec_file.csv', 'w') as f:
        f.write(txt)

    

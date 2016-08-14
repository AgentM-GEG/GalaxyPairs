# -*- coding: utf-8 -*-
import galaxy
import numpy as np
import csv

def writeCsvFile(fname, data, *args, **kwargs):
    """
    @param fname: string, name of file to write
    @param data: list of list of items

    Write data to file
    """
    mycsv = csv.writer(open(fname, 'wb'), *args, **kwargs)
    for row in data:
        mycsv.writerow(row)

def generateData(sample):
    '''
    Index:
    0 - TFIT ID 2
    1 - RA (radians)
    2 - Dec (radians)
    3 - Redshift
    4 - Mass (kg)
    '''
    data = np.genfromtxt(sample, dtype=None, names=True, delimiter =",")
    catalogDict = dict()
    for row in data:
        if (row['zspec'] != -99 and row['q_zspec'] ==1) or row['zspec'] == row['zbest']:
            gal = galaxy.galaxy(int(row['ID']), float(row['RAdeg']), float(row['DECdeg']), float(row['zspec']), float(np.log10(row['Median_Mass'])),float(row['Hmag']),float(row['zspec']),float(row['zspec']))
            catalogDict[gal.TFIT_ID] = [gal.RA, gal.Dec, gal.z, gal.radialComovingDistance(), gal.mass,gal.Hmag,gal.z_low,gal.z_up]
        else :
            gal = galaxy.galaxy(int(row['ID']), float(row['RAdeg']), float(row['DECdeg']), float(row['zphot']), float(np.log10(row['Median_Mass'])),float(row['Hmag']),float(row['photo_z_low']),float(row['photo_z_up']))
            catalogDict[gal.TFIT_ID] = [gal.RA, gal.Dec, gal.z, gal.radialComovingDistance(), gal.mass,gal.Hmag,gal.z_low,gal.z_up]
    return catalogDict

def generateCompanions(Comparesample):
    '''
    Index:
    0 - TFIT ID 2
    1 - RA (radians)
    2 - Dec (radians)
    3 - Redshift
    4 - Mass (kg)
    '''
    companions = np.genfromtxt(Comparesample, dtype=None, names=True, delimiter =",")
    companionDict = dict()
    for row in companions:
        if (row['zspec'] != -99 and row['q_zspec'] ==1) or row['zspec'] == row['zbest']:
            gal = galaxy.galaxy(int(row['ID']), float(row['RAdeg']), float(row['DECdeg']), float(row['zspec']), float(np.log10(row['Median_Mass'])),float(row['Hmag']),float(row['zspec']),float(row['zspec']))
            companionDict[gal.TFIT_ID] = [gal.RA, gal.Dec, gal.z, gal.radialComovingDistance(), gal.mass,gal.Hmag,gal.z_low,gal.z_up]
        else:
            gal = galaxy.galaxy(int(row['ID']), float(row['RAdeg']), float(row['DECdeg']), float(row['zphot']), float(np.log10(row['Median_Mass'])),float(row['Hmag']),float(row['photo_z_low']),float(row['photo_z_up']))
            companionDict[gal.TFIT_ID] = [gal.RA, gal.Dec, gal.z, gal.radialComovingDistance(), gal.mass,gal.Hmag,gal.z_low,gal.z_up]
    return companionDict

def angularSeparation(obj1, obj2):
    '''
    Outputs the angular separation (radians) between object 1 and 2.
    '''
    dRA = ((obj2[0] - obj1[0])**2)**(0.5)
    dDEC = ((obj2[1] - obj1[1])**2)**(0.5)
    avgDEC = (obj1[1] + obj2[1]) / 2.0
    return ((dDEC**2 + (dRA * np.cos(avgDEC))**2)**(0.5))

def transverseComovingDistance(obj1, obj2):
    '''
    (transverse)
    kpc
    '''
    radialDist = obj1[3]
    return radialDist * angularSeparation(obj1, obj2)
def identify_pairs(sample,Comparesample,Paircat):
    print ("Generating Data...")
    data = generateData(sample)
    print ("Data Generated... Generating Companions...")
    companions = generateCompanions(Comparesample)
    print ("Companions Generated... Calculating Pairs...")
    pairCatalog = [['host_id',
                'z_host',
                'comp_id',
                'z_comp',
                'delta_z',
                'mass_ratio',
                'SEP','Mass_host','Mass_comp','Hmag_host','Hmag_comp','zhost_l68','zhost_u68','zcomp_l68','zcomp_u68'
                ]]

    '''
    Calculates pairs based on a R_proj <= 50kpc using the redshift of the dominant
    (more massive) galaxy. The cosmology is listed in galaxy.py.
    '''
    n = 1
    for key1 in data:
        for key2 in companions:
            if key1 != key2:
                gal1 = data[key1]
                gal2 = companions[key2]
                aS = angularSeparation(gal1, gal2)
                #if aS < (2.5 * 10**(-5)): # A quick test to avoid unecessary calculations.
                if gal1[4] >= gal2[4]:
                    tCD = transverseComovingDistance(gal1, gal2)
                    if tCD <= 50:
                        delta_z = ((gal2[2] - gal1[2])**2)**0.5
                        mass_ratio = gal1[4] / gal2[4]
                        pairCatalog.append([key1, gal1[2], key2, gal2[2], round(delta_z, 3), round(mass_ratio, 3), round(tCD, 3),gal1[4],gal2[4],gal1[5],gal2[5],gal1[6],gal1[7],gal2[6],gal2[7]])
                    else:
                        pass
                else:
                    pass
                #else:
                    #pass
        print (n)
        n += 1

    


    
    writeCsvFile(Paircat, pairCatalog)
    print ("\nDone Writing File.")

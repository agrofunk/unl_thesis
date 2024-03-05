# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 20:20:35 2014

@author: denis
"""

import xuleta, time

shape = '/media/denis/GEO/DROUGHT_shapefiles/base_sojaPR/soja_diss_meso.shp'
root = '/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/baseline/'
ivs = ['ndi7','ndwi','sdi','vci']#,'vhi_70_3']#'evi'
rootout = '/home/denis/Copy/IPYdissertation/dados/baselines_micro2/'
stats = 'mean'

start1 = time.time()
for iv in ivs:
    start2 = time.time()
    folder = root + iv + '/media2/'
    out = rootout + 'micro_' + iv + '.csv'
    xuleta.rastastats(folder,shape,out,stats)
    folder, out = None, None
    print 'Tempo total: ' + str((time.time() - start2)/60.) + 'minutos'
    
print 'Tempo total: ' + str((time.time() - start1)/60.) + 'minutos'


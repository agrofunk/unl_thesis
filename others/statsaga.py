# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 02:34:05 2015

@author: denis
"""
import processing, xuleta, shutil, time, os

tempfolder = "/tmp/processing/"
folderout = "/media/denis/GEO/DROUGHT_shapefiles/statistics/indices/"
shape = "/media/denis/GEO/DROUGHT_shapefiles/base_sojaPR/soja_diss_micro.shp"
folders = ["/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/ndwi/",
"/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/ndi7/",
"/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/ndvi/",
"/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/evi/",
"/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/sdi/",
"/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/vci/",
"/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/FILTRADOS/vhi_70_3/"]
ind = ["ndwi","ndi7","ndvi","evi","sdi","vci","vhi"]

n=6
tempo0 = time.time()
tempo = time.time()
lista = xuleta.listfiles(folders[n],extension="*.tif",full=True)
print 'processando primeiro baloque de ' + ind[n]
do1 = processing.runalg("saga:gridstatisticsforpolygons",lista[0:180],shape,False,False,False,False,False,True,False,False,0,folderout + "micromean_" + ind[n] + "_1.shp")
print 'processamento do primeiro baloque de %s, demorou %.2f minutos' %(ind[n],(time.time()-tempo)/60)
if os.path.exists(tempfolder): shutil.rmtree(tempfolder)
tempo = time.time()
print 'processando segundo baloque ' + ind[n]
do2 = processing.runalg("saga:gridstatisticsforpolygons",lista[181:360],shape,False,False,False,False,False,True,False,False,0,folderout + "micromean_" + ind[n] + "_2.shp")
print 'processamento do segundo baloque de %s, demorou %.2f minutos' %(ind[n],(time.time()-tempo)/60)
if os.path.exists(tempfolder): shutil.rmtree(tempfolder)
tempo = time.time()
print 'processando urtimo baloque ' + ind[n]
do3 = processing.runalg("saga:gridstatisticsforpolygons",lista[361:],shape,False,False,False,False,False,True,False,False,0,folderout + "micromean_" + ind[n] + "_3.shp")
print 'processamento do urtimo baloque de %s, demorou %.2f minutos' %(ind[n],(time.time()-tempo)/60)
if os.path.exists(tempfolder): shutil.rmtree(tempfolder)
#lista, do1, do2, do3 = None, None, None, None
print 'FOICE, demorou %.2f' %(time.time()-tempo0)/60
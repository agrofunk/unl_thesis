import processing, xuleta, shutil,os
folder = '/media/denis/GEO/DROUGHT_processed/Vegetation_Indices/baseline/evi/mediana/'
tempfolder = "/tmp/processing/"
folderout = '/home/denis/Copy/IPYdissertation/dados/'
shape = "/media/denis/GEO/DROUGHT_shapefiles/base_sojaPR/soja_diss_micro.shp"
shape2 = '/media/denis/GEO/DROUGHT_shapefiles/baseParana_e_Brasil/microrregioes_PRr.shp'
lista = xuleta.listfiles(folder,full=True)
processing.runalg("saga:gridstatisticsforpolygons",lista,shape2,
                        False,False,False,False,False,True,False,False,0,
                        folderout + "mic.shp")
#if os.path.exists(tempfolder): shutil.rmtree(tempfolder)
print "Done!"
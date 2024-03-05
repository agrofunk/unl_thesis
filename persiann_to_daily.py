def cumday(folder,folderout,year):
    import glob, gdal, os, time, datetime, xuleta
    import numpy as np
    import bottleneck as bn
    
    year = str(year)
    lista = []
    listadata = []
    for j in glob.glob(folder + year + '*.tif'):
        b = j.split('/')
        c = b[-1]
        d = c[-19:-4]
        lista.append(c)
        listadata.append(d)
        lista.sort()
        listadata.sort()
        
    meses = []
    for i in listadata:
        meses.append(i[4:6])
        meses.sort()
    meses = [ii for n,ii in enumerate(meses) if ii not in meses[:n]]
    
    dias = []
    for i in listadata:
        dias.append(i[6:8])
        dias.sort()
    dias = [ii for n,ii in enumerate(dias) if ii not in dias[:n]]
    
    datum = gdal.Open(folder + lista[0])
    geo = datum.GetGeoTransform()
    proj = datum.GetProjection()
    col = datum.RasterYSize
    row = datum.RasterXSize
    shape = (row,col)
    driver = gdal.GetDriverByName( 'GTiff' )
    
    # ACUMULAR DIARIAMENTE #
    ########################
    if not os.path.exists(folderout): os.makedirs(folderout)
    
    start = time.time()
    for mes in meses:
        for dia in dias:
            toOpen = []
            for i in lista:
                if i[4:6] == mes and i[6:8] == dia:
                    toOpen.append(i)
            toOpen.sort()
            
            if toOpen == []:
                print 'skipping day ' + year + mes + dia
            else:
                arrays = []
                print 'Processing ' + year + mes + dia
                for j in toOpen:
                    imagem = gdal.Open(folder + j).ReadAsArray()
                    arrays.append(imagem)
                    arrays2 = np.dstack(arrays)   
                    
                soma = bn.nansum(arrays2, axis=2)
                
                im_saida = driver.Create(folderout + year +  mes + dia + '.tif', row, col, 1, gdal.GDT_Int16)
                im_saida.SetGeoTransform(geo)
                im_saida.SetProjection(proj)
                im_saida.GetRasterBand(1).WriteArray(soma)
                del im_saida, arrays2, arrays, toOpen, soma 

            #print 'Processing ' + year + mes + dia
    print 'Ano processado! Demorou a eternidade de %.2f' %((time.time() - start)/60)
    
folder = '/media/denis/seagate/PRECIPITATION/PERSIANN/daily_r/'
folderout = '/media/denis/seagate/PRECIPITATION/PERSIANN/daily/'
years = [x for x in range(2000,2015,1)]#2000,2015
for year in years:
    cumday(folder,folderout,year)
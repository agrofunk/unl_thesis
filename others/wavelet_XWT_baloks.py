# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 12:17:26 2015

@author: denis
"""

import pandas as pd
import sys, numpy, pylab #,pycwt
import warnings
warnings.simplefilter("ignore", numpy.ComplexWarning)
#import matplotlib.pyplot as plt
sys.path.append('/usr/local/lib/python2.7/dist-packages/pycwt/')
import wav as wavelet
import plot as wavplot
#%%
banco = '/home/denis/SPIDEROAK/IPYdissertation/dados/banco_diss.h5'
#regiao = 'OP_Toledo'
iv = 'lswi'
folder = '/home/denis/SPIDEROAK/dissertation/F_teste/'

#%%
dados = pd.read_hdf(banco, 'ivs/micro/' + iv)
chuvas = pd.read_hdf(banco, 'lstagri/microday_ma')

def boxpdf(x):
    """
    Forces the probability density function of the input data to have
    a boxed distribution.
    
    PARAMETERS
        x (array like) :
            Input data
    
    RETURNS
        X (array like) :
            Boxed data varying between zero and one.
        Bx, By (array like) :
            Data lookup table
    
    """
    x = numpy.asarray(x)
    n = x.size
    
    # Kind of 'unique'
    i = numpy.argsort(x)
    d = (numpy.diff(x[i]) != 0)
    I = pylab.find(numpy.concatenate([d, [True]]))
    X = x[i][I]
    
    I = numpy.concatenate([[0], I+1])
    Y = 0.5 * (I[0:-1] + I[1:]) / n
    bX = numpy.interp(x, X, Y)
    
    return bX, X, Y


#%%

#%%
def aswavelet(regiao):
    y1 = dados[regiao][4:512].tolist()
    y2 = chuvas[regiao][4:512].tolist()
    y2 = numpy.asarray(y2);y1 = numpy.asarray(y1)
    x2 = numpy.arange(0,len(y2),1);x1 = x2
    chuvas.columns
    mother = wavelet.Morlet()
    save = True
    
    s1 = y1;s2=y2;t1=x1;t2=x2
    dt = numpy.diff(t1)[0]
    n1 = t1.size
    n2 = t2.size
    n = min(n1, n2)
    s2, _, _ = boxpdf(s2)
    std1 = s1.std()
    std2 = s2.std()
    cwt1 = wavelet.cwt(s1 / std1, dt, wavelet=mother)
    sig1 = wavelet.significance(1.0, dt, cwt1[1], 0, 0.0,wavelet=mother)
    cwt2 = wavelet.cwt(s2 / std2, dt, wavelet=mother)
    sig2 = wavelet.significance(1.0, dt, cwt2[1], 0, 0.0,wavelet=mother)
    
    xwt = wavelet.xwt(t1, s1, t2, s2, significance_level=0.8646, 
                      result='full', normalize=True)
    wct = wavelet.wct(t1, s1, t2, s2, significance_level=0.8646, normalize=True)
    # Do the plotting!
    pylab.close('all')
    
    
    fig = wavplot.figure(ap=dict(left=0.07, bottom=0.06, right=0.95, 
        top=0.95, wspace=0.05, hspace=0.10))
    ax = fig.add_subplot(2, 1, 1)
    fig, ax = wavplot.cwt(t1, s1, cwt1, sig1, fig=fig, ax=ax, extend='both')
    ax.set_title(iv.upper(), y=0.9, fontweight='bold',color='w')    
    bx = fig.add_subplot(2, 1, 2, sharex=ax)
    bx.set_title('LST', y=0.9, fontweight='bold',color='w')
    fig, bx = wavplot.cwt(t2, s2, cwt2, sig2, fig=fig, ax=bx, extend='both')
    ax.set_xlim = ([t2.min(), t1.max()])
    if save:
        fig.savefig(folder+'wt_lst'+regiao+'_'+iv+'_cwt.png', bbox_inches='tight', dpi=300, format='png')
    
    fig = wavplot.figure(fp=dict())
    ax = fig.add_subplot(1, 1, 1)
    fig, ax = wavplot.xwt(*xwt, fig=fig, ax=ax, extend='both')
    ax.set_xlim = ([xwt[1].min(), xwt[1].max()])
    if save:
        fig.savefig(folder+'wt_lst'+regiao+'_'+iv+'_xwt.png', bbox_inches='tight', dpi=300, format='png')
    
    fig = wavplot.figure(fp=dict())
    ax = fig.add_subplot(1, 1, 1)
    fig, ax = wavplot.xwt(*wct, fig=fig, ax=ax, extend='neither',
        crange=numpy.arange(0, 1.1, 0.1), scale='linear', angle=wct[5])
    ax.set_xlim = ([wct[1].min(), wct[1].max()])
    if save:
        fig.savefig(folder+'wt_lst'+regiao+'_'+iv+'_wct.png', bbox_inches='tight', dpi=300, format='png')
    
    pylab.close('all')
    del ax, bx, xwt, std1,std2,fig,wct,sig1,sig2,s1,s2,t1,t2,dt
#%%
lista = ['OP_Toledo']
#IRO        
        #u'COCP_CampoM', u'COCP_Goioere',u'NCP_Faxinal',   u'NCP_Ivaipora',
        #u'OP_Cascavel', u'OP_Foz', u'OP_Toledo', 'NCP_Astorga',#u'NCP_Maringa',
        #u'NP_Assai'
#NAO IRO 
         # u'NCP_Florai', u'NCP_Londrina', u'NCP_Porecatu', u'NP_CornelioP',
         
for regiao in lista:
    aswavelet(regiao)
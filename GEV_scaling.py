# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:18:31 2022

@author: manis
"""
import numpy as np
import math as m
import pandas as pd

import skextremes as ske
from lmoments3 import distr as lm
import matplotlib.pyplot as plt

ams =pd.read_csv("C:/home/IITB/ELMUSK/P2/Temporal_downscaling/AMS.csv")
ams = ams.set_index("year")
daily = ams["HR24"]

def scaling(hr):
    s1hr=[1,1,1,1]
    s1hr[0]= np.log(47.49/5.36)/np.log(1/24)
    s1hr[1]= np.log(28.61/3.49)/np.log(1/24)
    s1hr[2]= np.log(20.97/2.67)/np.log(1/24)
    s1hr[3]= np.log(16.77/2.19)/np.log(1/24)
    
    s2hr=[1,1,1,1]
    s2hr[0]= np.log(31.26/5.36)/np.log(2/24)
    s2hr[1]= np.log(18.94/3.49)/np.log(2/24)
    s2hr[2]= np.log(13.92/2.67)/np.log(2/24)
    s2hr[3]= np.log(11.15/2.19)/np.log(2/24)
    
    s3hr=[1,1,1,1]
    s3hr[0]= np.log(23.74/5.36)/np.log(3/24)
    s3hr[1]= np.log(14.83/3.49)/np.log(3/24)
    s3hr[2]= np.log(11.14/2.67)/np.log(3/24)
    s3hr[3]= np.log(9.09/2.19)/np.log(3/24)
    
    s6hr=[1,1,1,1]
    s6hr[0]= np.log(15.53/5.36)/np.log(6/24)
    s6hr[1]= np.log(9.99/3.49)/np.log(6/24)
    s6hr[2]= np.log(7.64/2.67)/np.log(6/24)
    s6hr[3]= np.log(6.31/2.19)/np.log(6/24)
    
    s12hr=[1,1,1,1]
    s12hr[0]= np.log(9.4/5.36)/np.log(12/24)
    s12hr[1]= np.log(6.19/3.49)/np.log(12/24)
    s12hr[2]= np.log(4.79/2.67)/np.log(12/24)
    s12hr[3]= np.log(3.96/2.19)/np.log(12/24)
    
    if(hr==1):
        return(np.mean(s1hr))
    if(hr==2):
        return(np.mean(s2hr))
    if(hr==3):
        return(np.mean(s3hr))
    if(hr==6):
        return(np.mean(s6hr))
    if(hr==12):
        return(np.mean(s12hr))
    


def pwm_scaling(d,hr):
    model = ske.models.classic.GEV(d, fit_method = 'mle')
    
    if(hr==24):
        s=1
    else:
        s =scaling(hr)
        print(s)
    rt=[1,1,1,1,1]
    rt[0]=lm.gev.isf( 1./2,model.c,((hr/24)**s)*model.loc,((hr/24)**s)*model.scale)
    rt[1]=lm.gev.isf( 1./10,model.c,((hr/24)**s)*model.loc,((hr/24)**s)*model.scale)
    rt[2]=lm.gev.isf( 1./25,model.c,((hr/24)**s)*model.loc,((hr/24)**s)*model.scale)
    rt[3]=lm.gev.isf( 1./50,model.c,((hr/24)**s)*model.loc,((hr/24)**s)*model.scale)
    rt[4]=lm.gev.isf( 1./100,model.c,((hr/24)**s)*model.loc,((hr/24)**s)*model.scale)
    return(rt)

rt_HR01 = pwm_scaling(ams["HR24"].values/24,1)
rt_HR02 = pwm_scaling(ams["HR24"].values/24,2)
rt_HR03 = pwm_scaling(ams["HR24"].values/24,3)
rt_HR06 = pwm_scaling(ams["HR24"].values/24,6)
rt_HR12 = pwm_scaling(ams["HR24"].values/24,12)
rt_HR24 = pwm_scaling(ams["HR24"].values/24,24)
idf_dfs = pd.DataFrame(data= [rt_HR01,rt_HR02,rt_HR03,rt_HR06,rt_HR12,rt_HR24])

idf_dfs['Duration']= [1,2,3,6,12,24]
idf_dfs=idf_dfs.set_index('Duration')

idf_dfs = idf_dfs.rename(columns={0: '2 year',1: '10 year',2: '25 year',3: '50 year',4: '100 year',})
idf_dfs.plot()

def _plot(ax, title, xlabel, ylabel):
    
    # helper function for:
    #     self.plot_density()
    #     self.plot_pp()
    #     self.plot_qq()
    #     self.plot_return_values()
    #     self.plot_summary()
    ax.set_facecolor((0.95, 0.95, 0.95))
    plt.setp(ax.lines, linewidth = 2, color = 'magenta')
    ax.set_title(title,weight='bold', size=14)
    ax.set_xlabel(xlabel,weight='bold', size=14)
    ax.set_ylabel(ylabel,weight='bold', size=14)
    ax.grid(True)
    return ax

#print(sT,_ci_Td,_ci_Tu)
fig, ax = plt.subplots(figsize=(8, 6))


    
# plot
ax = _plot(ax, "Historical IDF", 'Duration (Hours)', 'Intensity (mm/hr)')
ax.plot(idf_dfs["2 year"],label = "2 Year")
ax.plot(idf_dfs["10 year"],label = "10 Year")
ax.plot(idf_dfs["25 year"],label = "25 Year")
ax.plot(idf_dfs["50 year"],label = "50 Year")
ax.plot(idf_dfs["100 year"],label = "100 Year")

ax.legend()
plt.savefig("C:/home/IITB/ELMUSK/P2/Temporal_downscaling/Historical_IDF_Check.png", dpi = 300)

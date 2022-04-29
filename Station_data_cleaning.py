# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 16:11:31 2022

@author: manish
"""

import pandas as pd
import numpy as np


import pymannkendall as mk

f="data_9.5_76.5"

##IMD##
#b2_2=["data_9.625_77.125","data_9.625_76.875","data_9.875_77.125","data_9.875_76.875"]
b2_2=["data_9.625_76.875"]

data1=np.genfromtxt("C:/home/IITB/ELMUSK/P1/Attribution_scripts/Attribution/Uncertainity/Attribution/Observation_based/data_9.625_76.875_IMD.txt")

daily=pd.DataFrame(data1[:,3],index = pd.date_range('01.01.1901',periods = len(data1[:,3]),freq ='D', name = 'date'),columns=["IMD"])

I=daily
IMD_ymax=I.groupby([I.index.year.rename('year') ]).max().dropna()

data2 = pd.read_excel("C:/home/IITB/MISC/IMD_Purchase/IMD_Purchase/16NOV/047_11/pr.xlsx",header = 0)

data = data2[[ 'HRF01', 'HRF02', 'HRF03', 'HRF04', 'HRF05', 'HRF06', 'HRF07', 'HRF08', 'HRF09', 'HRF10', 'HRF11',
             'HRF12', 'HRF13', 'HRF14', 'HRF15', 'HRF16', 'HRF17', 'HRF18', 'HRF19', 'HRF20', 'HRF21', 'HRF22', 'HRF23', 'HRF24']]

df = data.values.reshape(348984,1)

hourly=pd.DataFrame(df,index = pd.date_range('01.01.1979',periods = len(df),freq ='H', name = 'date'),columns=["IMD"])
hourly2 = hourly.resample('2H').sum()
hourly3 = hourly.resample('3H').sum()
hourly6 = hourly.resample('6H').sum()
hourly12 = hourly.resample('12H').sum()
hourly24 = hourly.resample('24H').sum()
#df = data2.values.reshape(494394)
max_1hr = hourly.groupby([hourly.index.year.rename('year') ]).max().dropna()

ams = hourly.groupby([hourly.index.year.rename('year') ]).max().dropna()

ams["HR01"] = hourly.groupby([hourly.index.year.rename('year') ]).max().dropna()
ams["HR02"] = hourly2.groupby([hourly2.index.year.rename('year') ]).max().dropna()
ams["HR03"] = hourly3.groupby([hourly3.index.year.rename('year') ]).max().dropna()
ams["HR06"] = hourly6.groupby([hourly6.index.year.rename('year') ]).max().dropna()
ams["HR12"] = hourly12.groupby([hourly12.index.year.rename('year') ]).max().dropna()
ams["HR24"] = hourly24.groupby([hourly24.index.year.rename('year') ]).max().dropna()
ams = ams.drop(["IMD"],axis=1)

ams.to_csv("C:/home/IITB/ELMUSK/P2/Temporal_downscaling/AMS.csv", index = True, header=True)

"""
2,10,25,50,100
"""
import skextremes as ske
from lmoments3 import distr as lm
import matplotlib.pyplot as plt


def rtp(h):
    model = ske.models.classic.GEV(h, fit_method = 'mle')
    rt=[1,1,1,1,1]
    rt[0]=lm.gev.isf( 1./2,model.c,model.loc,model.scale)
    rt[1]=lm.gev.isf( 1./10,model.c,model.loc,model.scale)
    rt[2]=lm.gev.isf( 1./25,model.c,model.loc,model.scale)
    rt[3]=lm.gev.isf( 1./50,model.c,model.loc,model.scale)
    rt[4]=lm.gev.isf( 1./100,model.c,model.loc,model.scale)
    return(rt)

rt_HR01 = rtp(ams["HR01"].values)
rt_HR02 = rtp(ams["HR02"].values/2)
rt_HR03 = rtp(ams["HR03"].values/3)
rt_HR06 = rtp(ams["HR06"].values/6)
rt_HR12 = rtp(ams["HR12"].values/12)
rt_HR24 = rtp(ams["HR24"].values/24)

idf_df = pd.DataFrame(data= [rt_HR01,rt_HR02,rt_HR03,rt_HR06,rt_HR12,rt_HR24])

idf_df['Duration']= [1,2,3,6,12,24]
idf_df=idf_df.set_index('Duration')

idf_df = idf_df.rename(columns={0: '2 year',1: '10 year',2: '25 year',3: '50 year',4: '100 year',})
idf_df.plot()

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
ax.plot(idf_df["2 year"],label = "2 Year")
ax.plot(idf_df["10 year"],label = "10 Year")
ax.plot(idf_df["25 year"],label = "25 Year")
ax.plot(idf_df["50 year"],label = "50 Year")
ax.plot(idf_df["100 year"],label = "100 Year")

ax.legend()
plt.savefig("C:/home/IITB/ELMUSK/P2/Temporal_downscaling/Historical_IDF.png", dpi = 300)

####loglog plot for break point


pwm = pd.read_excel("C:/home/IITB/ELMUSK/P2/Temporal_downscaling/PWM.xlsx",header = 0,sheet_name ="PWM")

loglog = pd.read_excel("C:/home/IITB/ELMUSK/P2/Temporal_downscaling/PWM.xlsx",header = 0,sheet_name ="loglog")
loglog = loglog.set_index("Duration")

###for scaling for linking 1 hour and 24 hour
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

model = ske.models.classic.GEV(daily, fit_method = 'mle')

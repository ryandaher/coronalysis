#!/usr/bin/env python
# coding: utf-8

# # Active Cases
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
from Visualizations import *
# In[ ]:


def activeCases(df,dfd,dfr):
    coactive = df-dfd-dfr
    coactive['Days'] = list(range(0,len(coactive)))
    return(coactive)


# # Differences

# In[10]:


def differences(df):
    rang = range(0,len(df)-1)
    diffd = {}
    for c in list(df.columns):
        listed = []
        for i in rang:
            listed.append(df[c][i+1]-df[c][i])
        diffd[c] = listed
    diffeddf = pd.DataFrame.from_dict(diffd)
    diffeddf['Days'] = [i for i in range(0,len(diffeddf))]
    return(diffeddf)


# # Growth Factor

# In[9]:


def growthFactor(diffdf):
    coronagr = {}
    for c in list(diffdf.columns):
        listgr = []
        for i in range(0,len(diffdf)-1):
            a = diffdf[c][i+1]
            b = diffdf[c][i]
            if b == 0:
                b = 1
                listgr.append(a/b)
            else:
                listgr.append(a/b)
        coronagr[c] = listgr
    coronagr = pd.DataFrame.from_dict(coronagr)
    coronagr['Days'] = [i for i in range(0,len(coronagr))]
    return(coronagr)


# # Percent Change

# In[8]:


def percentChange(df):
    rangp = range(0,len(df)-1)
    dictpc = {}
    for c in list(df.columns):
        listpc = []
        for i in rangp:
            a = df[c][i]
            b = df[c][i+1]
            f = b-a
            if a == 0:
                a = 1
                pc = (f/a)*100
            else:
                pc = (f/a)*100
            listpc.append(pc)
        dictpc[c] = listpc
    coronapc = pd.DataFrame.from_dict(dictpc)
    coronapc['Days'] = [i for i in range(0,len(coronapc))]
    return(coronapc)

def conbreak(df):
    from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2,map_countries
    ME = ['Bahrain','Cyprus','Egypt','Iran','Iraq','Israel','Jordan','Kuwait','Lebanon','Oman','Palestine','Israel','Qatar','Saudi Arabia','Syria','Turkey','United Arab Emirates','Yemen']
    AsiaC = [0 for i in range(0,len(df))]
    EuropeC = [0 for i in range(0,len(df))]
    AmericaC = [0 for i in range(0,len(df))]
    MEC = [0 for i in range(0,len(df))]
    OceanicC = [0 for i in range(0,len(df))]
    AfricaC = [0 for i in range(0,len(df))]
    SAmericaC = [0 for i in range(0,len(df))]
    otherC = [0 for i in range(0,len(df))]
    cocol = df.columns

    for i in cocol:
        if i not in ['Days', 'AsiaC', 'EuropeC', 'AmericaC', 'MEC','OceanicC', 'other','Others','Total']:
            if i in ME:
                MEC = MEC+df[i]
            elif (country_alpha2_to_continent_code(country_name_to_country_alpha2(i)) == 'AS'):
                AsiaC = AsiaC + df[i]
            elif (country_alpha2_to_continent_code(country_name_to_country_alpha2(i)) == 'EU'):
                EuropeC = EuropeC + df[i]
            elif (country_alpha2_to_continent_code(country_name_to_country_alpha2(i)) == 'AF'):
                AfricaC = AfricaC + df[i]
            elif (country_alpha2_to_continent_code(country_name_to_country_alpha2(i)) == 'OC'):
                OceanicC = OceanicC + df[i]
            elif (country_alpha2_to_continent_code(country_name_to_country_alpha2(i)) == 'NA'):
                AmericaC = AmericaC + df[i]
            elif (country_alpha2_to_continent_code(country_name_to_country_alpha2(i)) == 'SA'):
                SAmericaC = SAmericaC + df[i]
            else:
                otherC = otherC+df[i]
        else:
            otherC = otherC+df[i]
    continents = ['MEC','AsiaC','EuropeC','AfricaC','OceanicC','AmericaC','SAmericaC','otherC']
    continentsd = [MEC,AsiaC,EuropeC,AfricaC,OceanicC,AmericaC,SAmericaC,otherC]

    for i in range(0,len(continents)):
        df[continents[i]] = continentsd[i]

    df = df.fillna(0)
    df['AsiaC_C'] = df['AsiaC']-df['China']
    return(df)
# In[ ]:

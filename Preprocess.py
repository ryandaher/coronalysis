#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests


# # Scraping - Yesterday / Today Data

# In[9]:


def scraper(new = False):
    url = 'https://www.worldometers.info/coronavirus/#nav-yesterday'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    if new:
        df = df_list[0]
    df = pd.DataFrame(df)
    dfn = df[['Country,Other','TotalCases','TotalDeaths','TotalRecovered','ActiveCases']]
    dfn = dfn.T
    dfn.columns = dfn.iloc[0,:]
    dfn.drop('Country,Other',axis=0,inplace=True)
    dfn = dfn.fillna(0)
    dfn2 = dfn.copy()
    dfn2 = dfn2.drop(['Diamond Princess','Vatican City','Channel Islands','Aruba','Timor-Leste'],axis=1)
    dfn2.rename(columns={'Total:':'Total','Congo':'Republic of the Congo','Réunion':'Reunion','Cabo Verde':'Cape Verde','S. Korea':'South Korea','USA':'United States of America',
                            'CAR':'Central African Republic','DRC':'Democratic Republic of the Congo',"UK":'United Kingdom',
                            'UAE':'United Arab Emirates','St. Vincent Grenadines':'Saint Vincent and the Grenadines'},inplace=True)
    dfn2['United Kingdom'] = dfn2['United Kingdom']+ + dfn2['British Virgin Islands']+dfn2['Bermuda']+dfn2['Cayman Islands']+dfn2['Gibraltar']+dfn2['Isle of Man']+dfn2['Montserrat']+dfn2['Turks and Caicos']
    dfn2['China'] = dfn2['China']+dfn2['Hong Kong']+dfn2['Macao']
    dfn2['Netherlands'] = dfn2['Netherlands'] + dfn2['Curaçao']+dfn2['Sint Maarten']
    dfn2['Denmark'] = dfn2['Denmark']+dfn2['Faeroe Islands']
    dfn2['France'] = dfn2['France'] + dfn2['French Polynesia'] + dfn2['Saint Martin']+dfn2['New Caledonia'] + dfn2['St. Barth']
    dfn2.drop(['Bermuda','Cayman Islands','Gibraltar','Isle of Man','Montserrat','Turks and Caicos','Hong Kong',
                  'Macao','Curaçao','Sint Maarten','Faeroe Islands','French Polynesia','New Caledonia','St. Barth'],axis=1,inplace=True)
    dfn2['France'] = dfn2['France']+dfn2['French Guiana'] + dfn2['Guadeloupe'] + dfn2['Martinique'] + dfn2['Mayotte'] + dfn2['Reunion']+dfn2['Saint Martin']
    dfn2['Denmark'] = dfn2['Denmark']+dfn2['Greenland']
    dfn2.drop(['British Virgin Islands','French Guiana','Greenland','Guadeloupe','Martinique','Mayotte','Reunion','Saint Martin'],axis=1,inplace=True)
    if new:
        dfn = dfn2.copy()
        return(dfn)
    else:
        dfo = dfn2.copy()
        return(dfo)


# # Updating Datasets

# In[7]:


def newvals(df,dfd,dfr,dfnew,l1,l2,l3):
    coronac = df.append(pd.Series(),ignore_index=True)
    coronad = dfd.append(pd.Series(),ignore_index=True)
    coronar = dfr.append(pd.Series(),ignore_index=True)
    for i in df.columns:
        if i not in ['Days']:
            coronac[i].iloc[-1] = dfnew[i].loc['TotalCases']
            coronad[i].iloc[-1] = dfnew[i].loc['TotalDeaths']
            coronar[i].iloc[-1] = dfnew[i].loc['TotalRecovered']
    coronac['Days'] = list(range(0,len(coronac)))
    coronad['Days'] = list(range(0,len(coronad)))
    coronar['Days'] = list(range(0,len(coronar)))
    coronac.to_csv(l1,index=False)
    coronad.to_csv(l2,index=False)
    coronar.to_csv(l3,index=False)
    return(0)


# In[13]:


corona = pd.read_csv('covid1.csv')
codeath = pd.read_csv('codeath1.csv')
corecov = pd.read_csv('corecov.csv')


# In[10]:


newvals(corona,codeath,corecov,scraper(),'covid1.csv','codeath1.csv','corecov.csv')


# # Continent Breakdown

# In[28]:


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


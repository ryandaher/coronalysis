#!/usr/bin/env python
# coding: utf-8

# # Highest Cases Pie Chart
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
from Computations import *
import streamlit as st
# In[14]:


def pieWorst(diffdf,text):
    worst = diffdf.drop('Total',axis=1)
    pie = list(worst.iloc[-1,:].sort_values(ascending=False).iloc[:10])
    CD = diffdf.T
    a=CD.shape[1]-1
    names = [CD[CD[a]==i].index[0] for i in pie]
    fig = px.pie(diffdf, values=pie, names=names,title=text,color_discrete_sequence=px.colors.sequential.RdBu,width=810, height=600)
    fig.update_traces(textposition='inside', textinfo='value+label')
    return(fig)

def genBreak(active,recov,death):
    totalv=[active['Total'].iloc[-1], recov['Total'].iloc[-1], death['Total'].iloc[-1]]
    totaln=['Active','Recovered','Dead']
    fig = go.Figure([go.Bar(x=totaln, y=totalv,text=totalv,textposition='auto')])
    fig.update_layout(width=1200,height=600)
    return(fig)
# # General Information

# In[15]:


def generalInfo(df,carray):

    reg  = go.Figure()
    for country in carray:
        reg.add_trace(go.Scatter(x=df['Days'],y=df[country],name=country))
    reg.update_layout(xaxis_title='Days',yaxis_title='Cases',width=1200, height=600)
    st.write('### Number of Cases Over Time')
    st.write(reg)

    log = go.Figure()
    for country in carray:
        log.add_trace(go.Scatter(x=df['Days'],y=df[country],name=country))
    log.update_layout(xaxis_title='Days',yaxis_title='Cases',yaxis_type='log',width=1200, height=600)
    st.write('### Number of Cases Over Time (Log Scale)')
    st.write(log)


# # Growth Factor Analysis

# In[19]:


def gfComputation(dfg,carray,d):
    growthp = go.Figure()
    for country in carray:
        daverage = dfg[country].iloc[-d:].median()
        growthp.add_trace(go.Scatter(x=dfg['Days'],y=dfg[country],name=country))
        growthp.add_shape(type='line',x0=(dfg['Days'].iloc[-1]),x1=(dfg['Days'].iloc[-d]),y0=daverage,y1=daverage)
    growthp.update_layout(yaxis_title='Case Growth Rate',xaxis_title='Days',width=1200, height=600)
    st.write('### Growth Factor Over Time')
    st.write(growthp)
    for country in carray:
        daverage = dfg[country].iloc[-d:].median()
        st.write(country,daverage)


# In[20]:


def gfBar(dfg,carray,d):
    gfComputation(dfg,carray,d)
    bard = {}

    for country in carray:
        bard[country] = dfg[country].iloc[-d:].median()
    bard['Stable'] = 1
    bard = sorted(bard.items(), key=lambda x: x[1],reverse=True)

    xcol = []
    vals = []
    for i in range(0,len(bard)):
        xcol.append(bard[i][0])
        vals.append(bard[i][1])

    fig = px.bar(x=xcol, y=vals,height=400,color=xcol)

    fig.update_layout(xaxis_title='Country',yaxis_title='Growth Factor',width=1200, height=600)
    st.write('### Median Growth Factor in the Last',d,'Days')
    st.write(fig)


# # Full Depth Analysis

# In[18]:


def fullDepth(df,dfdiff,dfpc,dfg,carray):
    reg = go.Figure()
    log = go.Figure()
    diff = go.Figure()
    pc = go.Figure()
    growth = go.Figure()

    for country in carray:
        reg.add_trace(go.Scatter(x=df['Days'],y=df[country],name=country))
        log.add_trace(go.Scatter(x=df['Days'],y=df[country],name=country))
        diff.add_trace(go.Scatter(x=dfdiff['Days'],y=dfdiff[country],name=country))
        pc.add_trace(go.Scatter(x=dfpc['Days'],y=dfpc[country],name=country))
        growth.add_trace(go.Scatter(x=dfg['Days'],y=dfg[country],name=country,mode='markers'))

    growth.add_shape(type='line',x0=0,x1=len(dfg)-1,y0=1,y1=1,line=dict(
                color="purple",
                width=1))
    reg.update_layout(xaxis_title='Days',yaxis_title='Cases',width=1200, height=600)
    log.update_layout(xaxis_title='Days',yaxis_title='Log Cases',yaxis_type='log',width=1200, height=600)
    diff.update_layout(xaxis_title='Days',yaxis_title='New Cases',width=1200, height=600)
    pc.update_layout(xaxis_title='Days',yaxis_title='Percent Change',width=1200, height=600)
    growth.update_layout(xaxis_title='Days',yaxis_title='Growth Factor',width=1200, height=600)

    st.write('### Number of Cases Over Time')
    st.write(reg)
    st.write('### Number of Cases Over Time (Log Scale)')
    st.write(log)
    st.write('### Number of New Cases Over Time')
    st.write(diff)
    st.write('### Case Percent Change Over tume')
    st.write(pc)
    st.write('### Growth Factor Over Time')
    st.write(growth)


# # Case Breakdown

# In[33]:


def caseBreakdown(dfd,dfr,dfa):
    labels = ['Active Cases','Deaths','Recoveries',]
    dt = dfd.iloc[-1]
    rt = dfr.iloc[-1]
    at = dfa.iloc[-1]
    values = [at,dt,rt]
    night_colors = ['rgb(214, 213, 201)','rgb(10, 16, 13)', 'rgb(36, 106, 115)']

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, values=values, hole=.3,marker_colors=night_colors))

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(width=1200, height=600)
    st.write('Breakdown of Total Cases')
    st.write(fig)


# # Square Breakdown

# In[28]:


def squareBreakdown(df):
    import matplotlib
    import squarify # pip install squarify (algorithm for treemap)&lt;/pre&gt;
    acc = df[['EuropeC','AfricaC','AmericaC','OceanicC','AsiaC','SAmericaC','MEC']].sort_values(by=len(df)-1,axis=1,ascending=False)
    actc = ['Europe','North America','South America','Asia','Middle East','South America','Oceanic','Africa']
    actv = list(acc.iloc[-1,:])
    # Create a dataset:
    my_values=actv

    # create a color palette, mapped to these values
    cmap = matplotlib.cm.Blues
    mini=min(my_values)
    maxi=max(my_values)
    norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in my_values]

    # Change color

    # Draw Plot
    plt.figure(figsize=(12,8), dpi= 80)
    squarify.plot(sizes=my_values, label=actc, alpha=.9, color=colors )
    plt.axis('off')
    st.write("## Active Cases by Continent")
    st.pyplot()


# In[ ]:





# # Death Recovery Active Cases Timeline

# In[12]:


def draBreakdown(df,dfr,dfd,country):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Days'], y=dfr[country], fill='tonexty', fillcolor = 'rgb(0, 99, 93)',
                             mode='none',name='Recoveries'))
    fig.add_trace(go.Scatter(x=df['Days'], y=df[country], fill='tonexty',fillcolor='rgb(1, 23, 47)',
                             mode='none', name='Total Cases'))
    fig.add_trace(go.Scatter(x=df['Days'], y=dfd[country], fill='tozeroy',fillcolor='rgb(76, 33, 42)',
                             mode='none', name='Deaths'))

    fig.update_layout(xaxis_title='Days',yaxis_title='Number of People',width=1200, height=600)
    st.write('Breakdown Over Time')
    st.write(fig)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from Computations import *
from Visualizations import *
import string

#def extra():
#    padding-top: {padding_top}rem;
#
#    padding-bottom: {padding_bottom}rem;
#    color: {COLOR};
#    background-color: {BACKGROUND_COLOR};
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1500px;
        padding-right: 12rem;
        padding-left: 10rem;
    }}
    .reportview-container .main {{
        color: black;
        background-color: white;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


corona = pd.read_csv('covid1.csv')
codeath = pd.read_csv('codeath1.csv')
corecov = pd.read_csv('corecov1.csv')
active = activeCases(corona,codeath,corecov)

#coronaC = conbreak(corona)
codeathC = conbreak(codeath)
corecovC = conbreak(corecov)
activeC = conbreak(active)

coronadiff = differences(corona)
codeathdiff = differences(codeath)
corecovdiff = differences(corecov)
activediff = differences(active)

coronagf = growthFactor(coronadiff)
codeathgf = growthFactor(codeathdiff)
corecovgf = growthFactor(corecovdiff)
activegf = growthFactor(activediff)

coronapc = percentChange(corona)
codeathpc = percentChange(codeath)
corecovpc = percentChange(corecov)
activepc = percentChange(active)


st.title('COVID-19 Current Overview')
st.write('[Number of New Cases Since Yesterday] - [Current Active Cases , Recoveries, Deaths] - [Current Cases by Continent]')
ov = st.button('Show me the overview')
if ov:
    st.write('## Number of New Cases Since Yesterday')
    st.write(pieWorst(coronadiff,''))

    st.write('## Current Active Cases - Recoveries - Deaths')
    st.write(genBreak(active,corecov,codeath))

    squareBreakdown(activeC)
    if st.button('Hide',key='h1'):
        ov = False


st.title('Country Analysis & Comparisons')
st.write("(Quick Information shows cases over time. Deep Dive includes total cases, new cases, percent change, and growth factor over time.)")
st.write('### Select Country Names')
defa = ["United States of America", "Japan"]
countrylist = st.multiselect("Columns", corona.columns.tolist(), default=defa)
analysistype = st.radio("Basic or Deep Analysis?",('General Information', 'Deep Dive'))
abutt = st.button('Plot!')
if abutt:
    if (analysistype == 'General Information'):
        generalInfo(corona,countrylist)
    elif (analysistype == 'Deep Dive'):
        fullDepth(corona,coronadiff,coronapc,coronagf,countrylist)
    if st.button('Hide',key='h2'):
        abutt = False



st.title('Growth Factor Analysis')
st.write("(Generally, a growth factor above 1 indicates rapid/exponential growth, while 1 represents a stable/linear growth.)")
defag = ["China", "Spain"]
countrylistgf = st.multiselect("Columns", corona.columns.tolist(), default=defag)
Days = st.slider('Days to Analyse', 0, 14, 5)
gfbutton = st.button('Plot Growth Factor')
if gfbutton:
    gfBar(coronagf,countrylistgf,Days)
    if st.button('Hide',key='h3'):
        gfbutton = False

st.title('Active Cases - Deaths - Recoveries Breakdown')
countriesbd = st.selectbox('Select a Country',corona.columns)
#countriesbd = st.text_input("Enter Country Name", 'Lebanon')
breakdownb = st.button('Show Breakdown')
if breakdownb:
    caseBreakdown(codeath[countriesbd],corecov[countriesbd],active[countriesbd])
    draBreakdown(corona,corecov,codeath,countriesbd)
    if st.button('Hide',key='h4'):
        breakdownb = False

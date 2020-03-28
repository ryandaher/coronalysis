#!/usr/bin/env python
# coding: utf-8

# In[46]:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
from Computations import *
from Visualizations import *


active = activeCases(corona,codeath,corecov)


# ### Continents

# In[20]:


coronaC = conbreak(corona)
codeathC = conbreak(codeath)
corecovC = conbreak(corecov)
activeC = conbreak(active)


# ### Differencing

# In[21]:


coronadiff = differences(corona)
codeathdiff = differences(codeath)
corecovdiff = differences(corecov)
activediff = differences(active)


# ### Growth Factor

# In[22]:


coronagf = growthFactor(coronadiff)
codeathgf = growthFactor(codeathdiff)
corecovgf = growthFactor(corecovdiff)
activegf = growthFactor(activediff)


# ### Percent Change

# In[23]:


coronapc = percentChange(corona)
codeathpc = percentChange(codeath)
corecovpc = percentChange(corecov)
activepc = percentChange(active)


# # Visualizations

# In[24]:


pieWorst(coronadiff,'New Cases')


# In[25]:


generalInfo(corona,['Italy','Spain','United States of America'])


# In[26]:


gfBar(coronagf,['Spain','Italy','United States of America'],5)


# In[27]:


fullDepth(corona,coronadiff,coronapc,coronagf,['Spain','Italy','United States of America'])


# In[40]:


caseBreakdown(codeath[country],corecov[country],active[country],colorlist=['rgb(228, 223, 218)','rgb(35, 17, 35)', 'rgb(82, 150, 165)'])


# In[38]:


squareBreakdown(active,countrylist=['United States of America','Italy','Spain','Germany'])
#squareBreakdown()


# In[39]:


draBreakdown(corona,corecov,codeath,'United States of America')


# In[ ]:

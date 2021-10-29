#!/usr/bin/env python
# coding: utf-8

# **COVID Vaccination rate in relationship with GDP per capita and Human Development Index**

# The data has been taken from https://ourworldindata.org/covid-vaccinations on August 2021. It includes the vaccination statistics for each country, and I combined it with the GDP (Gross Domestic Product) per capita and HDI (Human Development Index) of each country to see if the vaccination rollout for developed and developing countries is different.

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# In[3]:


import pandas as pd

df_pop = pd.read_excel('COVID-19-geographic-disbtribution-worldwide.xlsx')
df_pop = df_pop[['country_code', 'population2019']].drop_duplicates()

df_gdp_country = pd.read_excel('gdp.xlsx')

df_gdp = df_gdp_country.merge(df_pop, how='inner', on='country_code')
df_gdp['GDP per capita'] = round(1000000*(df_gdp['GDP'] / df_gdp['population2019']),2)

#missing data inserted from: 
#http://data.un.org/Data.aspx?q=New+Caledonia&d=SNAAMA&f=grID%3A101%3BcurrID%3AUSD%3BpcFlag%3A1%3BcrID%3A540

df_gdp.loc[df_gdp['country_code'] == 'VGB', ['GDP per capita']] = 43189
df_gdp.loc[df_gdp['country_code'] == 'PYF', ['GDP per capita']] = 21567
df_gdp.loc[df_gdp['country_code'] == 'NCL', ['GDP per capita']] = 34942
df_gdp.loc[df_gdp['country_code'] == 'SSD', ['GDP per capita']] = 448
df_gdp.loc[df_gdp['country_code'] == 'ERI', ['GDP per capita']] = 567
df_gdp.loc[df_gdp['country_code'] == 'SYR', ['GDP per capita']] = 1194
df_gdp.loc[df_gdp['country_code'] == 'VEN', ['GDP per capita']] = 4733


# In[4]:


df = pd.read_csv('owid-covid-data.csv')


# In[6]:


df2 = df[['iso_code', 'continent', 'location', 'date', 'total_vaccinations', 
           'people_vaccinated', 'people_fully_vaccinated',
          'life_expectancy', 'human_development_index']]


# In[7]:


g = df2.groupby('location')
g = g['people_fully_vaccinated'].max()


# In[8]:


a = 0
t = {}
for a in range(0,len(g)):
    t[g.index[a]] = g[a]
    


# In[9]:


df_a = pd.DataFrame.from_dict(t, orient='index', columns=['people_fully_vaccinated'])
df_a['location'] = df_a.index
df_a.reset_index(level=0, inplace=True)
df_a = df_a.drop(columns=['index'])


# In[10]:


a = ['Africa', 'Asia', 'European Union', 
     'Europe', 'International', 'North America', 
     'Oceania', 'South America', 'World']
df_n = df_a[~df_a['location'].isin(a)]


# In[11]:


df_fully_vacc = df_n.merge(df2, how='inner', on=['people_fully_vaccinated', 'location'])
df_fully_vacc = df_fully_vacc.drop(columns=['date', 'total_vaccinations', 'people_vaccinated'])
df_fully_vacc = df_fully_vacc.drop_duplicates().reset_index()
df_fully_vacc = df_fully_vacc.dropna()


# In[12]:


df_vacc = df_gdp.merge(df_fully_vacc[['iso_code', 'people_fully_vaccinated', 'continent', 'life_expectancy', 
                                      'human_development_index']], 
                       how='inner', 
                       left_on = 'country_code', 
                       right_on = 'iso_code')


# In[13]:


df_vacc['fully_vaccinated%'] = round(100*(df_vacc['people_fully_vaccinated'] / df_vacc['population2019']), 2)


# In[14]:


df_vacc['GDP per capita Group'] = pd.cut(df_vacc['GDP per capita'], 
                                         bins=[0, 2000, 5000, 10000, 35000, 150000], 
                                         labels=['0 - 2000','2001 - 5000','5001 - 10,000','10,001 - 35,000', 'more than 35,000'])
#df_vacc.insert(5,'GDP per capita Group',category)
df_vacc = df_vacc.dropna()
df_vacc['human_development_index'] = round(df_vacc['human_development_index'], 2)


# The relationship between people fully vaccinated and GDP per capita for each country shows that more than 40% of people are fully vaccinated in most countries with a GDP per capita of more than 35,000. Whereas most countries with GDP per capita 2000 or less, the vaccination rate is lower than 20%.

# In[15]:


import plotly.express as px
fig = px.scatter(df_vacc, x='fully_vaccinated%', y='GDP per capita', 
                 size='fully_vaccinated%', color='GDP per capita Group',
                 hover_name='country', 
                 category_orders={'GDP per capita Group': ['0 - 2000','2001 - 5000','5001 - 10,000','10,001 - 35,000', 'more than 35,000']}, 
                 hover_data=['continent', 'GDP', 'population2019'], 
                 title='People Fully Vaccinated(%) and GDP per capita by Countries')
#log_x=True, log_y=True, size_max=20)
fig.show()


# The relationship between people fully vaccinated and Human Development Index (HDI) for each country shows that for most of the countries the higher the HDI value, the higher the percentage of fully vaccinated people.

# In[16]:


fig = px.scatter(df_vacc, x='fully_vaccinated%', y='human_development_index', 
                 size='fully_vaccinated%', color='human_development_index',
                 hover_name='country', hover_data=['continent'], 
                title='People Fully Vaccinated(%) and Human Development Index by Countries')
fig.show()


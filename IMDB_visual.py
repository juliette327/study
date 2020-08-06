#!/usr/bin/env python
# coding: utf-8

# In[116]:


from pylab import rcParams
rcParams['figure.figsize'] = 10,7

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns


# In[20]:


movies = pd.read_csv('tmdb_5000_movies.csv')
movies.head()


# In[28]:


movies['profit'] = movies['revenue'] - movies['budget']
movies.head()


# In[41]:


movies.release_date = pd.to_datetime(movies['release_date'])
movies['year'] = movies.release_date.dt.year
movies.head()


# In[46]:



from pandas.io.json import json_normalize
import json
def json_decode(data,key):
    
    """
Description: This function can be used to helpful to perform decoding in Python of JSON string.

Arguments:
    data: the data that we want decoding. 
    key: the key that we want to return its value.

Returns:
    list of values
"""
    result = []
    data = json.loads(data) #convert to jsonjsonn from string
    for item in data: #convert to list from json
        result.append(item[key])
    return result


# In[47]:


movies.genres = movies.genres.apply(json_decode,key='name')


# In[48]:


movies.keywords = movies.keywords.apply(json_decode,key='name')


# In[50]:


movies.production_companies = movies.production_companies.apply(json_decode,key='name')


# In[51]:


movies.head()


# In[97]:


movies_year = movies.groupby(['year']).sum()
mm = movies_year.sort_values('revenue', ascending=False).head(15)
mm


# In[ ]:


# Box-Office, TOP-15 years - выделить наиболее кассовые года для киноиндустрии, видим, что пропыв случился в 2012 года, в год выпуска Аватара


# In[106]:


mm['revenue'].plot(kind='bar', rot=45)


# In[ ]:


#Box-Office vs Profit vs Budget - отобразить динамику затрат на производство, выручки и кассовых сборов для фильмов по годам.
#На данной диаграмме удобно сравнивать динамику основных финансовых показателей кинокартин, видно, что прибыль киностудий начала расти со второй половины 2000х годов. 
#Возможно, это связано с допуском иностранных кинокартин на китайский рынок и с бумом открытия кинотеатров нового поколения по всему миру.


# In[110]:


plt.figure(figsize=(20, 8))
plt.plot(movies_year.index, movies_year['revenue'], label = 'Box-Office')
plt.plot(movies_year.index, movies_year['profit'], label = 'Profit')
plt.plot(movies_year.index, movies_year['budget'], label = 'Budget')
plt.xlabel('year'); plt.ylabel('Box-Office'); plt.title('Box-Office vs Revenue vs Budget')
plt.legend();


# In[ ]:


# Total Score Distribution - показать, какие оценки какие чаще всего ставят в фильмам.
# Можно предположить, что если фильм превзошел рейтинг 7.0, то он попал в 20% любимчиков аудиории. И к этому рейтингу стоит стремиться.


# In[117]:


ax = movies.vote_average.hist()
ax.set_title('User Score distribution')
ax.set_xlabel('user score')
ax.set_ylabel('movies')


# In[ ]:


# Score Distribution vs Revenue - как соотносятся кассовые сборы фильмов с их оценками
# Можно убедиться в корректности гипотезы о том, что если фильм удается, то благодаря сарафанному радио у него хорошие сборы в кинотеатрах.
# Оба графика имеют более-менее нормальное распределение, на них прослеживается довольно четкая связь между высокими рейтингами и высоким бокс-офисом


# In[120]:


sns.jointplot(x='vote_average', y='revenue', 
              data=movies, kind='scatter')


# In[ ]:


# Score Distribution vs Budget - как соотносятся оценки фильмов с их бюджетами на производство. 
#Выбрала heat, чтобы выдвинуть гипотезу о том, что высокие бюджеты кинонакартин далеко не всегда переходят в качество и в зрительскую любовь


# In[126]:


movies_rating_budget = movies.pivot_table(
                        index='year', 
                        columns='vote_average', 
                        values='budget', 
                        aggfunc=sum).fillna(0).applymap(float)

movies_rating_budget


# In[128]:


ax = sns.heatmap(movies_rating_budget)


# In[ ]:





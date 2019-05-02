import numpy as np
import pandas as pd
import re

# pLotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.grid_objs import Grid, Column
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import tools
# init_notebook_mode(connected=True)

import nltk

nltk.download('stopwords')

# LDA
import pyLDAvis
import pyLDAvis.gensim
from nltk.corpus import stopwords

stop = stopwords.words('english')
# pyLDAvis.enable_notebook()
from gensim import corpora, models

from scipy import stats

import warnings

warnings.filterwarnings('ignore')
import plotly.offline as pyo

# pyo.init_notebook_mode()

#-----------------------------------------------------------------------------------------------------------
twitter_tweets = pd.read_csv('tweets.csv')
fake_users = pd.read_csv('users.csv')
tweets_details = pd.read_csv('tweetdetails.csv')
#-----------------------------------------------------------------------------------------------------------

# clean the date to a Year-month format
fake_users['Date'] = pd.to_datetime(fake_users['created_at'])
fake_users = fake_users[pd.notnull(fake_users['created_at'])]
fake_users = fake_users.drop_duplicates(subset=['id'])
fake_users['Date'] = fake_users['Date'].apply(lambda x: x.strftime('%Y-%m'))

u_name = pd.DataFrame(fake_users.name.str.split(' ', 1).tolist(), columns=['first', 'last'])
user_name = u_name.groupby('first', as_index=False).size().reset_index(name='counts')
users_name = user_name.sort_values('counts', ascending=False).head(20)

# bar plot
# first names
first_name = u_name.groupby('first', as_index=False).size().reset_index(name='counts')
first_name = first_name.sort_values('counts', ascending=False).head(20)
df = go.Bar(
    x=first_name['counts'],
    y=first_name['first'],
    orientation='h',
    name='First name',
)

# last names
last_name = u_name.groupby('last', as_index=False).size().reset_index(name='counts')
last_name = last_name.sort_values('counts', ascending=False).head(20)
df1 = go.Bar(
    x=last_name['counts'],
    y=last_name['last'],
    orientation='h',
    name='Last name',
)

fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('First Name', 'Last Name'))
fig.append_trace(df, 1, 1)
fig.append_trace(df1, 2, 1)
fig['layout'].update(height=800, width=900, title='First and Last Names of Fake Accounts')
plot(fig, filename='basic-line')
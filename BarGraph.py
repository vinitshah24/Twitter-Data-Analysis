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

# -----------------------------------------------------------------------------------------------------------
twitter_tweets = pd.read_csv('tweets.csv')
fake_users = pd.read_csv('users.csv')
tweets_details = pd.read_csv('tweetdetails.csv')
# -----------------------------------------------------------------------------------------------------------

# clean the date to a Year-month format
fake_users['Date'] = pd.to_datetime(fake_users['created_at'])
fake_users = fake_users[pd.notnull(fake_users['created_at'])]
fake_users = fake_users.drop_duplicates(subset=['id'])
fake_users['Date'] = fake_users['Date'].apply(lambda x: x.strftime('%Y-%m'))

u_name = pd.DataFrame(fake_users.name.str.split(' ', 1).tolist(), columns=['first', 'last'])
user_name = u_name.groupby('first', as_index=False).size().reset_index(name='counts')
users_name = user_name.sort_values('counts', ascending=False).head(20)
# -----------------------------------------------------------------------------------------------------------

# group by date, create a count and sort
users = fake_users.groupby('Date', as_index=False).size().reset_index(name='counts')
users = users.sort_values('Date')

trace0 = go.Bar(
    name="Accounts Created Over TIme",
    x=users.Date,
    y=users.counts)
data = ([trace0])

layout = go.Layout(
    title="Accounts created 2009-2017",
    yaxis=dict(
        title='No. of Accounts created',
        range=[0, 100],
        titlefont=dict(
            size=20,
        )
    ),

    xaxis=dict(
        title='Year',
        range=['2009-01', '2017-1'],
        titlefont=dict(
            size=20,
        )
    )
)

fig = go.Figure(data=data, layout=layout)
fig['layout'].update()
plot(fig, filename='bar-graph')
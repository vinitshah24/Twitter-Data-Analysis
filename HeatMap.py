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

# heat map showing the days and hours of users
m = pd.pivot_table(tweets_details, values='user_key', index='created_strDayofweek',
                   columns='created_strMonth', aggfunc=len, fill_value=0, dropna=False)

z = m.as_matrix()

trace = go.Heatmap(z=z,
                   x=[i for i in np.arange(0, 24)],
                   y=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                   colorscale='Jet'
                   )
layout = go.Layout(
    title='No. of Tweets Per Day Per Month',
    xaxis=dict(
        nticks=24,
        title='Month',
        titlefont=dict(
            size=20)),
    yaxis=dict(
    ),
)
data = [trace]
fig = go.Figure(data=data, layout=layout)
fig['layout'].update()
plot(fig, filename='tweets.html')
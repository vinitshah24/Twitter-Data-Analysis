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

# remove the special characters
des = fake_users.description.copy().astype(str)
des = des.str.replace('[^\w\s]', '')
des = des.str.replace('[\\r|\\n|\\t|_]', ' ')
des = des.str.strip()

tweets_des = tweets_details.copy()
tweets_des.des = des
tweets_des.des = tweets_des.des.apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in (stop)]))

# convert sample documents into a list
doc_set = tweets_des.des.values.copy()

# Loop through document list
texts = [text.split(' ') for text in doc_set]

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenied documents into a document-term matrix
corp = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = models.ldamodel.LdaModel(corp, num_topics=30, id2word=dictionary)

df3 = pyLDAvis.gensim.prepare(ldamodel, corp, dictionary)

pyLDAvis.save_html(df3, 'DistanceMap.html')

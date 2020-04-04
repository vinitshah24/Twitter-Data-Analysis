import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
import os

csv_dir = os.path.join(os.path.dirname(__file__), 'data')
html_dir = os.path.join(os.path.dirname(__file__), 'templates')

tweets_file = os.path.join(csv_dir, 'tweets.csv')
users_file = os.path.join(csv_dir, 'users.csv')
tweets_details_file = os.path.join(csv_dir, 'tweetdetails.csv')

twitter_tweets = pd.read_csv(tweets_file)
fake_users = pd.read_csv(users_file)
tweets_details = pd.read_csv(tweets_details_file)

# clean the date to a Year-month format
fake_users['Date'] = pd.to_datetime(fake_users['created_at'])
fake_users = fake_users[pd.notnull(fake_users['created_at'])]
fake_users = fake_users.drop_duplicates(subset=['id'])
fake_users['Date'] = fake_users['Date'].apply(lambda x: x.strftime('%Y-%m'))

u_name = pd.DataFrame(
    fake_users.name.str.split(' ', 1).tolist(), columns=['first', 'last']
)
user_name = u_name.groupby(
    'first', as_index=False).size().reset_index(name='counts')
users_name = user_name.sort_values('counts', ascending=False).head(20)

# heat map showing the days and hours of users
m = pd.pivot_table(tweets_details,
                   values='user_key',
                   index='created_strDayofweek',
                   columns='created_strMonth',
                   aggfunc=len, fill_value=0, dropna=False)

trace = go.Heatmap(z=m,
                   x=[i for i in np.arange(0, 24)],
                   y=['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                       'Thursday', 'Friday', 'Saturday'],
                   colorscale='Jet'
                   )
layout = go.Layout(
    title='No. of Tweets Per Day Per Month',
    xaxis=dict(
        nticks=24,
        title='Month',
        titlefont=dict(size=20)
    ),
    yaxis=dict(
    ),
)
data = [trace]
fig = go.Figure(data=data, layout=layout)
fig['layout'].update()

output = os.path.join(html_dir, 'heat-map.html')
plot(fig, filename=output)

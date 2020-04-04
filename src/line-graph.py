import pandas as pd
import plotly.graph_objs as go
from plotly import tools
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

u_name = pd.DataFrame(fake_users.name.str.split(
    ' ', 1).tolist(), columns=['first', 'last'])
user_name = u_name.groupby(
    'first', as_index=False).size().reset_index(name='counts')
users_name = user_name.sort_values('counts', ascending=False).head(20)

# bar plot
# first names
first_name = u_name.groupby(
    'first', as_index=False).size().reset_index(name='counts')
first_name = first_name.sort_values('counts', ascending=False).head(20)
df = go.Bar(
    x=first_name['counts'],
    y=first_name['first'],
    orientation='h',
    name='First name',
)

# last names
last_name = u_name.groupby(
    'last', as_index=False).size().reset_index(name='counts')
last_name = last_name.sort_values('counts', ascending=False).head(20)
df1 = go.Bar(
    x=last_name['counts'],
    y=last_name['last'],
    orientation='h',
    name='Last name',
)

fig = tools.make_subplots(
    rows=2, cols=1, subplot_titles=('First Name', 'Last Name'))
fig.append_trace(df, 1, 1)
fig.append_trace(df1, 2, 1)
fig['layout'].update(height=800, width=900,
                     title='First and Last Names of Fake Accounts')

output = os.path.join(html_dir, 'line-graph')
plot(fig, filename=output)

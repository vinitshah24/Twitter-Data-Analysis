import pandas as pd
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

u_name = pd.DataFrame(fake_users.name.str.split(
    ' ', 1).tolist(), columns=['first', 'last'])
user_name = u_name.groupby(
    'first', as_index=False).size().reset_index(name='counts')
users_name = user_name.sort_values('counts', ascending=False).head(20)
print(users_name)

# group by date, create a count and sort
users = fake_users.groupby(
    'Date', as_index=False).size().reset_index(name='counts')
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

output = os.path.join(html_dir, 'bar-graph')
plot(fig, filename=output)

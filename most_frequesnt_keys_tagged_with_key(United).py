import tweepy
import operator
import matplotlib.pyplot as plt
import plotly.plotly as py
from heapq import nlargest
from collections import defaultdict
from basic_functions import *


# save_settings('access.json', access)
access = read_from_file('my_access.json')
auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
auth.set_access_token(access['access_token'], access['access_secret'])

api = tweepy.API(auth)

limit, query = 15000, '@united'
cursor = tweepy.Cursor(api.search, q=query, since="2017-04-10", until="2017-04-13", lang='en').items(limit)
tweets = get_tweets('tweets_in_April_by_keyword_United.json', load_existing=False, cursor_obj=cursor)  # load tweets locally

keywords, total = defaultdict(int), len(tweets)

# Do some pre-processing
for i, tweet in enumerate(tweets):
    # tags = [tag['text'] for tag in tweet['entities']['hashtags']]
    for tag_info in tweet['entities']['hashtags']:
        tag = tag_info['text']
        keywords[tag] += 1

# Find most popular complementary keywords and sort them by value
most_popular = {key: keywords[key] for key in nlargest(30, keywords, key=keywords.get)}
tags, tags_values = sorted(most_popular, key=most_popular.get, reverse=True), sorted(most_popular.values(), reverse=True)

# Plot collected info
x, y = range(1, len(tags) + 1), tags_values
labels = tags

# Add values at the top of the bars
for a, b in zip(x, y):
    plt.text(a, b + 40, str(b), ha='center', size='9')

plt.bar(x, y, color=list('rgbckym'))
# You can specify a rotation for the tick labels in degrees or with keywords.
plt.xticks(x, labels, rotation='vertical')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.12)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.45)
plt.xlabel('Keywords in tweets')
plt.ylabel('Keyword frequency')
plt.title('Statistics about most frequent tags together with tag "United" (during April)')

# plt.grid(True)
plt.show()

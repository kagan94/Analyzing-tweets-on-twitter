import json
import tweepy
import dateutil.parser
import matplotlib.pyplot as plt
import plotly.plotly as py
from datetime import datetime as dt


def save_to_file(file_name, obj):
    with open(file_name, 'w') as f:
        f.write(json.dumps(obj))


def read_from_file(file_name):
    with open(file_name, 'r') as f:
        obj = json.loads(f.read())
    return obj


def get_tweets(load_existing=True):
    # Request new tweets
    if load_existing is not True:
        place_id = api.geo_search(query="Estonia", granularity="country")[0].id
        query = (' place:%s' % place_id)

        tweets = tweepy.Cursor(api.search,
                               q=query,
                               since="2017-03-01", until="2017-04-01",
                               lang='en').items()
        # limit = 15
        # tweets = tweets.items(limit)
        found_tweets = [status for status in tweets]

        # Save tweets to file
        tweets_json = [tweet._json for tweet in found_tweets]
        save_to_file('tweets.json', tweets_json)

    # Read tweets from file
    tweets = read_from_file('tweets.json')
    return tweets


def get_total_by_keys(tweets, keywords):
    total = 0
    for tweet in tweets:
        if any(keyword in tweet['text'] for keyword in keywords):
            total += 1
    return total


# save_settings('access.json', access)
access = read_from_file('my_access.json')
auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
auth.set_access_token(access['access_token'], access['access_secret'])

api = tweepy.API(auth)

# tweets = get_tweets(load_existing=False)
tweets = get_tweets()  # load tweets locally
total = len(tweets)

stats_by_days = {day: 0 for day in range(32)}

# Do some pre-processing
for i, tweet in enumerate(tweets):
    # Parse only day from "created_at" and increment the # of published tweets on this day
    timestamp = dateutil.parser.parse(tweet['created_at']).timestamp()
    created_at_day = int(dt.fromtimestamp(timestamp).strftime('%d'))
    stats_by_days[created_at_day] += 1

    # Modify all text in lowercase
    tweets[i]['text'] = tweet['text'].lower()


# Count # of tweets by different keys
total_uni = get_total_by_keys(tweets, ['university', 'uni'])
total_tartu = get_total_by_keys(tweets, ['tartu'])
total_tartu_uni = get_total_by_keys(tweets, ['university of tartu', 'tartu uni', 'tartu university'])
total_tallinn_uni = get_total_by_keys(tweets, ['university of tallinn', 'tallinn uni', 'tallinn university', 'ttu', 'TTÜ'])


# Plot collected info
y = [total_uni, total_tartu, total_tartu_uni, total_tallinn_uni]
labels = ['Uni', 'Tartu', 'Tartu uni', 'Tallinn uni']
x = range(len(y))

fig, ax = plt.subplots()
ax.bar(x, y, width=1/1.5, color=list('rgbkym'))
ax.set_xticklabels(['', '', 'Uni', '', 'Tartu', '', 'Tartu uni', '', 'Tallinn uni'])

plt.legend(bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.)
plt.title('Statistics about published tweets by certain keywords (during March in Estonia)')
plt.xlabel('Keywords')
plt.ylabel('Number of tweets')

print('Total tweets: ', total)
print('keyword: uni: ', total_uni)
print('keyword: tartu: ', total_tartu)
print('keyword: tartu uni: ', total_tartu_uni)
print('keyword: tallinn uni: ', total_tallinn_uni)

# Plot stats about distribution of tweets during March in Estonia
# plt.xlabel('Days')
# plt.ylabel('Number of tweets')
# plt.title('Statistics by published tweets during March in Estonia')
# plt.plot(list(stats_by_days.keys()), list(stats_by_days.values()), 'g')

plt.grid(True)
plt.show()

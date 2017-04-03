import json
import tweepy
from tweepy import OAuthHandler


def save_settings(file_name, obj):
    with open(file_name, 'w') as f:
        f.write(json.dumps(obj))


def read_settings(file_name):
    with open(file_name, 'r') as f:
        obj = json.loads(f.read())
    return obj


# save_settings('access.json', access)
access = read_settings('my_access.json')

auth = OAuthHandler(access['consumer_key'], access['consumer_secret'])
auth.set_access_token(access['access_token'], access['access_secret'])
api = tweepy.API(auth)

# Read our own timeline
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status._json)
    print(status.text)


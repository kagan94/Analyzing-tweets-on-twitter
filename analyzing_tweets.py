import json
import tweepy


def save_to_file(file_name, obj):
    with open(file_name, 'w') as f:
        f.write(json.dumps(obj))


def read_from_file(file_name):
    with open(file_name, 'r') as f:
        obj = json.loads(f.read())
    return obj


# save_settings('access.json', access)
access = read_from_file('my_access.json')

auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
auth.set_access_token(access['access_token'], access['access_secret'])
api = tweepy.API(auth)

# Request to get tweets
query, max_tweets = 'Tartu', 5
found_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]

# Save/Read tweets to/from file
# found_tweets_json = [tweet._json for tweet in found_tweets]
# save_to_file('tweets.json', found_tweets_json)
# found_tweets = read_from_file('tweets.json')

for tweet in found_tweets:
    print(tweet.text, end='\n\n')
    print('isTruncated: ', tweet.truncated, end='\n\n')

    # print(tweet['text'], end='\n\n')
    # print('isTruncated: ', tweet['truncated'], end='\n\n')

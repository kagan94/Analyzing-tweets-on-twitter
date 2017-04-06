import json
import tweepy
import time


def save_to_file(file_name, obj):
    with open(file_name, 'w') as f:
        f.write(json.dumps(obj))


def read_from_file(file_name):
    with open(file_name, 'r') as f:
        obj = json.loads(f.read())
    return obj


def get_tweets(filename, load_existing=True, cursor_obj=None):
    # Request new tweets
    if load_existing is not True:
        # place_id = api.geo_search(query="Estonia", granularity="country")[0].id
        # query = (' place:%s' % place_id)
        assert cursor_obj != None

        print('start fetching tweets...')
        tweets, iter_num = [], 0
        while True:
            try:
                tweet = cursor_obj.next()
                tweets.append(tweet)

                iter_num += 1
                print(iter_num)
            except tweepy.TweepError:
                print('error')
                time.sleep(60*15)
                continue
            except StopIteration:
                break

        # Save tweets to file
        tweets_json = [tweet._json for tweet in tweets]
        save_to_file(filename, tweets_json)

    # Read tweets from file
    tweets = read_from_file(filename)
    return tweets


def total_by_keys(tweets, keywords):
    total = 0
    for tweet in tweets:
        if any(keyword in tweet['text'] for keyword in keywords):
            total += 1
    return total

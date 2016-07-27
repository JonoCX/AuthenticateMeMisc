__author__ = "Jonathan Carlton"

import tweepy
import re
from random import shuffle
import requests
import json
from os import path

# tweepy setup items
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
twitter_user = 'JonoCX56'

# monkeylearn setup items
monkeylearn_token = ''
monkeylearn_classifier_url = 'https://api.monkeylearn.com/v2/classifiers/'
monkeylearn_extractor_url = 'https://api.monkeylearn.com/v2/extractors/'
monkeylearn_lang = 'cl_hDDngsX8'
monkeylearn_topic = 'cl_5icAVzKR'
monkeylearn_extractor = 'ex_y7BPYzNG'


def key_setup(file_name="access-keys"):
    file_path = path.relpath(file_name)
    with open(file_path) as f:
        str = f.read()
        split = str.split("\n")
        consumer_key = split[0]
        consumer_secret = split[1]
        access_token = split[2]
        access_token_secret = split[3]
        monkeylearn_token = split[4]

key_setup()
# setup tweepy api client
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)

def fetch_tweets(api, twitter_user, tweet_type='timeline', max_tweets=200, min_words=5):
    tweets = []
    full_tweets = []
    step = 200
    for start in xrange(0, max_tweets, step):
        end = start + step
        count = min(step, max_tweets - start)
        kwargs = {'count': count}
        if full_tweets:
            last_id = full_tweets[-1].id
            kwargs['max_id'] = last_id - 1

        if tweet_type == 'timeline':
            current = api.user_timeline(twitter_user, **kwargs)
        else:
            current = api.favorites(twitter_user, **kwargs)

        full_tweets.extend(current)

    # for tweet in full_tweets:
    #     text = re.sub(r'(https?://\S+)', '', tweet.text)
    #     score = tweet.favorite_count + tweet.retweet_count
    #     if tweet.in_reply_to_status_id_str:
    #         score -= 15
    #
    #     if len(re.split(r'[^0-9A-Za-z]+', text)) > min_words:
    #         tweets.append((text, score))
    #
    #     #print tweet.text
    #     #print score
    #     #print '\n'

    return full_tweets

#tweets = fetch_tweets(api, twitter_user, 'timeline')
#tweets.extend(fetch_tweets(api, twitter_user, 'timeline', 1000)) # 400 = 2 request (out of 15 in the window)

#tweet_text = []
#for t in tweets:
#    tweet_text.append(t.text)

def classify_tweets(text_list, classifier_id):
    results = []
    step = 250
    for start in xrange(0, len(text_list), step):
        end = start + step
        data = {'text_list': text_list[start:end]}
        response = requests.post(
            monkeylearn_classifier_url + classifier_id + '/classify/',
            data=json.dumps(data),
            headers={
                'Authorization': 'Token {}'.format(monkeylearn_token),
                'Content-type': 'application/json'
            }
        )

        try:
            results.extend(response.json()['result'])
        except:
            print response.text
            raise

    return results

#res = classify_tweets(tweet_text, monkeylearn_topic)
#for r in res:
#    print r



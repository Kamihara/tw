#!/usr/bin/env python
# -*- coding:utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
from urllib.parse import urlparse
import mysql.connector


### Constants
oath_key_dict = {
    "consumer_key": "80YQXOcVFpvwPMSLcZWWWCxa2",
    "consumer_secret": "eHgq8LMhM3mvRl9IaetO6coOVkSZWJGAS6oOpZYxPAlDngLyw1",
    "access_token": "179552447-tkDDUZrWrVImMQKUFieHpeiNiDQqVvGIYhnDTntM",
    "access_token_secret": "RgFWV7LTDVEajIHPG0nQaPzvBp9zanbTiANq1XX0EHvPn"
}

url = urlparse('mysql://root:root@localhost:3306/km')

### Functions
def main():
    tweets_with_user = tweet_search_with_user("dayukoume", oath_key_dict)
    # print(tweets_with_user)
    for tweet in tweets_with_user:
        tweet_id = tweet[u'id_str']
        text = tweet[u'text']
        created_at = tweet[u'created_at']
        user_id = tweet[u'user'][u'id_str']
        user_description = tweet[u'user'][u'description']
        screen_name = tweet[u'user'][u'screen_name']
        user_name = tweet[u'user'][u'name']

        print("tweet_id:", tweet_id)
        print("text:", text)
        print("created_at:", created_at)
        print("user_id:", user_id)
        print("user_desc:", user_description)
        print("screen_name:", screen_name)
        print("user_name:", user_name)

        try:
            cur.execute('INSERT IGNORE INTO tweets'
                        ' (tweet_id, text, created_at, user_id, user_desc, screen_name, user_name)'
                        ' VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        [tweet_id, text, created_at, user_id, user_description, screen_name, user_name])
            conn.commit()
        except:
            conn.rollback()
            raise


    tweets_with_word = tweet_search_with_word("#まいにちチクショー", oath_key_dict)
    for tweet in tweets_with_word["statuses"]:
        tweet_id = tweet[u'id_str']
        text = tweet[u'text']
        created_at = tweet[u'created_at']
        user_id = tweet[u'user'][u'id_str']
        user_description = tweet[u'user'][u'description']
        screen_name = tweet[u'user'][u'screen_name']
        user_name = tweet[u'user'][u'name']
        # print("tweet_id:", tweet_id)
        # print("text:", text)
        # print("created_at:", created_at)
        # print("user_id:", user_id)
        # print("user_desc:", user_description)
        # print("screen_name:", screen_name)
        # print("user_name:", user_name)

        try:
            cur.execute('INSERT IGNORE INTO tweets'
                        ' (tweet_id, text, created_at, user_id, user_desc, screen_name, user_name)'
                        ' VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        [tweet_id, text, created_at, user_id, user_description, screen_name, user_name])
            conn.commit()
        except:
            conn.rollback()
            raise

    print("finished")

    return

def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

def tweet_search_with_word(search_word, oath_key_dict):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": search_word,
        "lang": "ja",
        "result_type": "recent",
        "count": "100"
        }
    oath = create_oath_session(oath_key_dict)
    response = oath.get(url, params = params)
    if response.status_code != 200:
        print("Error code: %d" %(response.status_code))
        return None
    tweets = json.loads(response.text)
    return tweets

def tweet_search_with_user(search_user, oath_key_dict):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        "screen_name": search_user,
        "lang": "ja"
        }
    oath = create_oath_session(oath_key_dict)
    response = oath.get(url, params = params)
    if response.status_code != 200:
        print("Error code: %d" %(response.status_code))
        return None
    tweets = json.loads(response.text)
    return tweets


### Execute
if __name__ == "__main__":
    conn = mysql.connector.connect(
        host = url.hostname or 'localhost',
        port = url.port or 3306,
        user = url.username or 'root',
        password = url.password or '',
        database = url.path[1:]
    )

    cur = conn.cursor()

    main()

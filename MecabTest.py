#!/usr/bin/env python
# -*- coding:utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
from urllib.parse import urlparse
import mysql.connector
import MeCab

### Constants
url = urlparse('mysql://root:root@localhost:3306/km')

### Functions
def main():
    sql = 'select text from tweets where screen_name = "dayukoume"'
    cur.execute(sql)
    tweet_texts = cur.fetchall()
    for text in tweet_texts:
        c_text = text[0].replace('\n', '')
        print("full text : " + c_text)

        mecabTagger = MeCab.Tagger("-Ochasen")
        node = mecabTagger.parseToNode(c_text)
        while node:
            word = node.surface
            # hinshi = node.feature
            hinshi = node.feature.split(",")[0]
            print(word + ": " + hinshi)
            node = node.next

    print("finished")

    return

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

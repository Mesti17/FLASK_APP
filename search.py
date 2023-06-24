from flask import Flask, render_template, request
import tweepy
import mysql.connector
import re
import snscrape.modules.twitter as sntwitter

app = Flask(__name__, template_folder="templates", static_url_path='/static')

def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    # remove non ASCII (emoticon, chinese word. etc)
    text = text.encode('ascii', 'replace').decode('ascii')
    return text


def searchTweets(query):
    content = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > 100:
            break
        username = tweet.user.username
        pesan = tweet.content.encode("utf-8")
        pesan_cleaned = cleanTxt(pesan.decode("utf-8"))
        content.append({
                'Username': username,
                'Tweet': pesan_cleaned,
            })
    
    return content


def cariTweet(message):
    tweets = searchTweets(message)
    return tweets


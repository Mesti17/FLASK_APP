from flask import Flask, render_template, request
import tweepy
import mysql.connector
import re
import snscrape.modules.twitter as sntwitter
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__, template_folder="templates", static_url_path='/static')

#Load Model
model_path = 'model/model_nb.pickle'
model = pickle.load(open(model_path, "rb"))

#Load Vectorizer
vectorizer = TfidfVectorizer()
with open('model/vec.pickle', 'rb') as handle:
    vectorizer = pickle.load(handle)

def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    # remove non ASCII (emoticon, chinese word. etc)
    text = text.encode('ascii', 'replace').decode('ascii')
    return text


def searchTweets(query):
    # teks = tweet
    # vec = vectorizer.transform([teks])
    # prediksi = model.predict(vec)

    # if prediksi == 1:
    #     hasil = 'POSITIF'
    # elif prediksi == 0:
    #     hasil = 'NETRAL'
    # else:
    #     hasil = 'NEGATIF'
        
    content = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > 100:
            break
        username = tweet.user.username
        pesan = tweet.content.encode("utf-8")
        pesan_cleaned = cleanTxt(pesan.decode("utf-8"))
        
        #prediksi tweet
        vec = vectorizer.transform([pesan_cleaned])
        prediksi = model.predict(vec)
        
        if prediksi == 1:
            hasil = 'POSITIF'
        elif prediksi == 0:
            hasil = 'NETRAL'
        else:
            hasil = 'NEGATIF'
        
        content.append({
                'Username': username,
                'Tweet': pesan_cleaned,
                'Label': hasil
            })
    
    return content


def cariTweet(message):
    tweets = searchTweets(message)
    return tweets


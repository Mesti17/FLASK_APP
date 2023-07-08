from flask import Flask, render_template, request
import tweepy
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Table, MetaData
import pymysql
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

# def cleanTxt(text):
#     text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
#     text = re.sub('#', '', text)  # Removing '#' hash tag
#     text = re.sub('RT[\s]+', '', text)  # Removing RT
#     text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
#     # remove non ASCII (emoticon, chinese word. etc)
#     text = text.encode('ascii', 'replace').decode('ascii')
#     return text


def searchTweets(keyword):
    
    engine = create_engine('mysql+pymysql://root:@localhost:3306/capres')
    # conn1 = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    # #Using pymysql

    table_name = 'hasil_preprocessing'  # Replace with the actual table name
    specific_word = keyword  # Replace with the specific word you want to search

    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    # conn2 = pymysql.connect(host='localhost', port=int(3306), user='root', password='', db='capres')

    query = table.select().where(table.c.cleaning.like(f'%{specific_word}%')).limit(100)
    results = session.execute(query)


    for result in results:
        print(result.username, result.cleaning)
    
    return content


def cariTweet(message):
    tweets = searchTweets(message)
    return tweets


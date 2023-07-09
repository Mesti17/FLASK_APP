from flask import Flask, flash, redirect, url_for, render_template, request, send_from_directory
from search import cariTweet
import re
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import json

app = Flask(__name__, template_folder="templates", static_url_path='/static')

#Load Model
model_path = 'model/model_nb.pickle'
model = pickle.load(open(model_path, "rb"))

#Load Vectorizer
vectorizer = TfidfVectorizer()
with open('model/vec.pickle', 'rb') as handle:
    vectorizer = pickle.load(handle)

# def sentimen_tweet(tweet):
    
#     teks = tweet
#     vec = vectorizer.transform([teks])
#     prediksi = model.predict(vec)

#     if prediksi == 1:
#         hasil = 'POSITIF'
#     elif prediksi == 0:
#         hasil = 'NETRAL'
#     else:
#         hasil = 'NEGATIF'
        
#     return hasil

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/prosescari", methods=['GET', "POST"])
def prosescari():

    if request.method == "POST":
        message = request.form['hashtag']
        hasil_cari, total_sentimen = cariTweet(message)
        
        # hasil_pred = cariTweet(message)

    return render_template(
        "hasil.html",
        data=hasil_cari,
        kata_pencarian=message,
        total=len(hasil_cari),
        total_sentimen=json.dumps(total_sentimen),
        total_pos=json.dumps(total_sentimen["Total_Pos"]),
        total_net=json.dumps(total_sentimen["Total_Net"]),
        total_neg=json.dumps(total_sentimen["Total_Neg"])
        )


# @app.route("/proseshasil", methods=['GET', "POST"])
# def proseshasil():

#     if request.method == "POST":
#         message = request.form['hashtag']
#         hasil_cari = cariTweet(message)

#     return render_template("hasil.html", data=hasil_cari, kata_pencarian=message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, flash, redirect, url_for, render_template, request, send_from_directory
from search import cariTweet
import re

app = Flask(__name__, template_folder="templates", static_url_path='/static')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/prosescari", methods=['GET', "POST"])
def prosescari():

    if request.method == "POST":
        message = request.form['hashtag']
        hasil_cari = cariTweet(message)

    return render_template("hasil.html", data=hasil_cari, kata_pencarian=message, total=len(hasil_cari))


# @app.route("/proseshasil", methods=['GET', "POST"])
# def proseshasil():

#     if request.method == "POST":
#         message = request.form['hashtag']
#         hasil_cari = cariTweet(message)

#     return render_template("hasil.html", data=hasil_cari, kata_pencarian=message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

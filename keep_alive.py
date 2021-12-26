from flask import Flask
from flask import render_template
from threading import Thread
import traceback
import sys
import os

"""
Required for starting the Flask application to keep bot open
Uptimerobot.com set to ping the host every 20 minutes to prevent
"""


app = Flask(__name__, template_folder='uptime')


@app.route("/")
def main():
    #return "Your bot is online!"
    return render_template("home.html")


def run():
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
    #app.run(port=8080, host='0.0.0.0')
    #https://stackoverflow.com/questions/18374138/how-to-show-index-html-page-in-heroku-using-python-flask

def keep_alive():
    server = Thread(target=run)
    server.start()

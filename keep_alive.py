from flask import Flask
from threading import Thread
import traceback
import sys

"""
Required for starting the Flask application to keep bot open
Uptimerobot.com set to ping the host every 20 minutes to prevent
"""


app = Flask("")


@app.route("/")
def main():
    return "Your bot is online!"


def run():
    app.run(host="127.0.0.1", port=8080)


def keep_alive():
    print('Keep Alive Started')
    server = Thread(target=run)
    server.start()

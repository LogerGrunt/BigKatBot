from flask import Flask
from threading import Thread
import traceback
import sys
import os

"""
Required for starting the Flask application to keep bot open
Uptimerobot.com set to ping the host every 20 minutes to prevent
"""


app = Flask("")


@app.route("/")
def main():
    return "Your bot is online!"


def run():
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')

def keep_alive():
    server = Thread(target=run)
    server.start()

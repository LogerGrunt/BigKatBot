from flask import Flask
from threading import Thread

"""
Required for starting the Flask application to keep bot open
Uptimerobot.com set to ping the host every 20 minutes to prevent
"""


app = Flask("")


@app.route("/")
def main():
    return "Your bot is online!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()

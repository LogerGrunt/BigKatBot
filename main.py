import os
import nextcord
import logging
from nextcord.ext import commands
import keep_alive
import subprocess

heroku_app_name = "bigkatbot"
raw_db_url = subprocess.run(
    ["heroku", "config:get", "DATABASE_URL", "--app", heroku_app_name],
    capture_output=True  # capture_output arg is added in Python 3.7
).stdout 
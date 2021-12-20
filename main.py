import os
import nextcord
import logging
from nextcord.ext import commands
import keep_alive
import psycopg2
from urllib.parse import urlparse

try:

    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    con = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    # Open a cursor to perform database operations
    cur = con.cursor()

    # Execute a query
    cur.execute("CREATE TABLE IF NOT EXISTS discordbot (keyname, value)")

    print "Database connection passed."


except:
    print "Database connection failed."

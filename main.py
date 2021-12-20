#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import nextcord
import logging
import keep_alive
import psycopg2
import urllib.parse as urlparse
from nextcord.ext import commands

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

    print("Database connection passed.")
except:

    print("Database connection failed.")


try:

    # Open a cursor to perform database operations

    cur = con.cursor()

    # Execute a query

    cur.execute("INSERT INTO discordbot (keyname, value) VALUES ('Test1', 'test2')")

    # Read

    print("SQL Passed.")
except:

    print("SQL Failed.")


# result_set = cur.execute("SELECT * FROM discordbot")

# for r in result_set:
#    print(r)

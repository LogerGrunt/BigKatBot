#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import nextcord
import logging
import keep_alive
import psycopg2
import urllib.parse as urlparse
from nextcord.ext import commands

con = None
cur = None

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
    con.autocommit = True

    print("Database connection passed.")
except:

    print("Database connection failed.")


try:

    # Open a cursor to perform database operations

    cur = con.cursor()

    # Execute a query

    # cur.execute("INSERT INTO discordbot (keyname, value) VALUES ('Test1', 'test2')")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (first_name text, last_name text, company text)"
    )
    cur.execute(
        "INSERT INTO users (first_name, last_name, company) VALUES ('Sam', 'Pitcher', 'Looker')"
    )

    print("SQL Passed.")
except:

    print("SQL Failed.")


try:

    # Open a cursor to perform database operations

    cur = con.cursor()

    # Read
    result_set = cur.execute("SELECT * FROM users")
    for r in result_set:
        print(r)

    # Read

    print("SQL-1 Passed.")
except:

    print("SQL-1 Failed.")
# result_set = cur.execute("SELECT * FROM discordbot")

# for r in result_set:
#    print(r)

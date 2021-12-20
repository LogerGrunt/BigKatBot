#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import nextcord
import logging
from nextcord.ext import commands
import keep_alive
import psycopg2
from urllib.parse import urlparse

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

cur.execute("INSERT INTO discordbot (keyname, value) VALUES ('Test1', 'test2')")

# Read

result_set = cur.execute("SELECT * FROM discordbot")

for r in result_set:
    print(r)



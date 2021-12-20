#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import nextcord
import logging
import keep_alive
#import urllib.parse as urlparse
from nextcord.ext import commands
from sqlalchemy import create_engine


uri = os.getenv("DATABASE_URL")  # or other relevant config var
#if uri.startswith("postgres://"):
#    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

try:

    db = create_engine(uri)

    print("Database connection passed.")
except:

    print("Database connection failed.")


try:

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

    # Read
    result_set = cur.execute("SELECT * FROM users")
    for r in result_set:
        print(r)

    # Read

    print("SQL-1 Passed.")
except:

    print("SQL-1 Failed.")

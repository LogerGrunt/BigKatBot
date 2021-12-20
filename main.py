#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import nextcord
import logging
import keep_alive

# import urllib.parse as urlparse
from nextcord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

try:

    db = scoped_session(sessionmaker(bind=uri))

    print("Database connection passed.")
except:

    print("Database connection failed.")


try:

    db.execute(
        "CREATE TABLE IF NOT EXISTS users (first_name text, last_name text, company text)"
    )
    db.commit()

    db.execute(
        "INSERT INTO users (first_name, last_name, company) VALUES ('Sam', 'Pitcher', 'Looker')"
    )
    db.commit()

    print("SQL Passed.")
except:

    print("SQL Failed.")


try:

    # Read
    result_set = db.execute("SELECT * FROM users")
    for r in result_set:
        print(r)

    # Read

    print("SQL-1 Passed.")
except:

    print("SQL-1 Failed.")

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nextcord
import logging
import keep_alive
import psycopg2
import urllib.parse as urlparse
from nextcord.ext import commands

class DiscordDB:

    def __init__(self):
        self.con = None
        self.cur = None

        def Connect(self):

            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port

            self.con = psycopg2.connect(dbname=dbname, user=user,
                    password=password, host=host, port=port)
            self.con.autocommit = True

        def setDB(self, keyname, value):

            self.cur = self.con.cursor()

            self.cur.execute("DELETE FROM discordbot WHERE keyname='%s';"
                             , keyname)
            self.cur.execute('INSERT INTO discordbot (keyname, value) VALUES (%s, %s);'
                             , (keyname, value))

        def Close(self):

            self.con.close()

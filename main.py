import os
import nextcord
import logging
from nextcord.ext import commands
import keep_alive
import psycopg2
from urllib.parse import urlparse

try:
    urlparse.uses_netloc.append("postgres") 
    connection_params = urlparse.urlparse(os.environ["DATABASE_URL"])
    db_connection = psycopg2.connect(database = connection_params.path[1:], user = connection_params.username, password = connection_params.password, host = connection_params.hostname, port = connection_params.port)
	print "Database connection passed."
except:
    print "Database connection failed."
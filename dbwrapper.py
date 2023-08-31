import sqlite3
from sqlite3 import Error
import logging

log = logging.getLogger('root')

#https://stackoverflow.com/questions/37648667/python-how-to-initiate-and-close-a-mysql-connection-inside-a-class

class DiscordDB(object):
    def __init__(self):
        self.dbfile = 'bot_database.db'
        self.con = None
        self.cur = None

    def __enter__(self):
        # This ensure, whenever an object is created using "with"
        # this magic method is called, where you can create the connection.
        try:
            self.con = sqlite3.connect('bot_database.db') # file path
            self.cur = self.con.cursor()
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

        return self
    
    def __exit__(self, exception_type, exception_val, trace):
        # once the with block is over, the __exit__ method would be called
        # with that, you close the connnection
        try:
           self.cur.close()
           self.con.close()
        except AttributeError: # isn't closable
           return True # exception handled successfully

    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    def CheckTables(self):
        try:
            self.cur.executescript(""" 
                CREATE TABLE IF NOT EXISTS CHANNELS(guild_id BIGINT, keyname VARCHAR(255), value VARCHAR(255));
                CREATE TABLE IF NOT EXISTS MOVIENIGHT(id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id BIGINT, link TEXT, watched BOOLEAN DEFAULT FALSE, fame BOOLEAN  DEFAULT FALSE);
            """)
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)
    
    def SetChannel(self, guild_id, keyname, value):
        try:
            self.cur.execute(
                "DELETE FROM CHANNELS WHERE guild_id = ? AND keyname = ?;", (guild_id, keyname,)
            )
            self.cur.execute(
                "INSERT INTO CHANNELS (guild_id, keyname, value) VALUES (?, ?, ?);", (guild_id, keyname, value,)
            )
            self.con.commit()

        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def GetChannel(self, guild_id, keyname):
        try:
            self.cur.execute(
                "SELECT value FROM CHANNELS WHERE guild_id = ? AND keyname = ?;", (guild_id, keyname,)
            )
            result = self.cur.fetchone()

            if result is not None:
                return result[0]
            else:
                return None
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Add(self, guild_id, value):
        try:
            self.cur.execute(
                "INSERT INTO MOVIENIGHT (guild_id, link) VALUES (?, ?);", (guild_id, value,)
            )
            self.con.commit()
            self.cur.execute(
                "SELECT last_insert_rowid() FROM MOVIENIGHT;"
            )
            result = self.cur.fetchone()

            if result is not None:
                return result[0]
            else:
                return None
            
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Get(self, guild_id, value):
        try:
            if self.is_integer(value) is True:
                self.cur.execute(
                    "SELECT * FROM MOVIENIGHT WHERE guild_id = ? AND id = ?;", (guild_id, value,)
                )
            else:
                self.cur.execute(
                    "SELECT * FROM MOVIENIGHT WHERE guild_id = ? AND link = ?;", (guild_id, value,)
                )

            result = self.cur.fetchone()

            if result is not None:
                return result
            else:
                return None
            
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Remove(self, guild_id, value):
        try:
            self.cur.execute(
                "DELETE FROM MOVIENIGHT WHERE guild_id = ? AND id = ?;", (guild_id, value,)
            )
            self.con.commit()

        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Random(self, guild_id):
        try:
            self.cur.execute(
                "SELECT * FROM MOVIENIGHT WHERE guild_id = ? AND watched = FALSE ORDER BY RANDOM() LIMIT 1;", (guild_id,)
            )
            result = self.cur.fetchone()

            if result is not None:
                return result
            else:
                return None
            
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Watched(self, guild_id, value, switch):
        try:
            self.cur.execute(
                "UPDATE MOVIENIGHT SET watched = ? WHERE guild_id = ? AND id = ?;", (switch, guild_id, value,)
            )
            self.con.commit()

            #check for changes
            if self.cur.rowcount < 1:
                return False
            else:
                return True

        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Fame(self, guild_id, value, switch):
        try:
            self.cur.execute(
                "UPDATE MOVIENIGHT SET fame = ? WHERE guild_id = ? AND id = ?;", (switch, guild_id, value,)
            )
            self.con.commit()

            #check for changes
            if self.cur.rowcount < 1:
                return False
            else:
                return True

        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def MovieNight_Find(self, guild_id, value):
        try:
            #SUBMOVIELIST is the alias name for the subquery
            numrows = self.cur.execute(
                "SELECT * FROM (SELECT * FROM MOVIENIGHT WHERE guild_id = ?) SUBMOVIELIST WHERE link LIKE ? LIMIT 10;", (guild_id, '%'+value+'%',)
            )
            result = self.cur.fetchall()

            #len of results will return the amount of rows
            if result is not None and len(result) > 0:
                return result
            else:
                return None
            
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def Commit(self):
        self.con.commit()

    def Close(self):
        try:
           self.cur.close()
           self.con.close()
        except AttributeError: # isn't closable
           return True # exception handled successfully



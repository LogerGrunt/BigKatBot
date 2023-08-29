import sqlite3
from sqlite3 import Error
import logging

log = logging.getLogger('root')

class DiscordDB:
    def __init__(self):
        self.con = None
        self.cur = None

    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()
        
    def Connect(self):
        try:
            self.con = sqlite3.connect('bot_database.db') # file path
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

        self.cur = self.con.cursor()
        return self.con

    def CheckTables(self):
        try:
            self.Connect()
            self.cur.executescript(""" 
                CREATE TABLE IF NOT EXISTS CHANNELS(guild_id BIGINT, keyname VARCHAR(255), value VARCHAR(255));
                CREATE TABLE IF NOT EXISTS MOVIENIGHT(id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id BIGINT, link TEXT, watched BOOLEAN DEFAULT FALSE, fame BOOLEAN  DEFAULT FALSE);
            """)
            self.Close()
        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)
    
    def SetChannel(self, guild_id, keyname, value):
        try:
            self.Connect()
            self.cur.execute(
                "DELETE FROM CHANNELS WHERE guild_id = ? AND keyname = ?;", (guild_id, keyname,)
            )
            self.cur.execute(
                "INSERT INTO CHANNELS (guild_id, keyname, value) VALUES (?, ?, ?);", (guild_id, keyname, value,)
            )
            self.con.commit()
            self.con.close()

        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)

    def GetChannel(self, guild_id, keyname):
        try:
            self.Connect()
            self.cur.execute(
                "SELECT value FROM CHANNELS WHERE guild_id = ? AND keyname = ?;", (guild_id, keyname,)
            )
            result = self.cur.fetchone()
            self.con.close()

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
            self.Connect()
            self.cur.execute(
                "INSERT INTO MOVIENIGHT (guild_id, link) VALUES (?, ?);", (guild_id, value,)
            )
            self.con.commit()
            self.cur.execute(
                "SELECT last_insert_rowid() FROM MOVIENIGHT;"
            )
            result = self.cur.fetchone()
            self.con.close()

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
            self.Connect()
            if self.is_integer(value) is True:
                self.cur.execute(
                    "SELECT * FROM MOVIENIGHT WHERE guild_id = ? AND id = ?;", (guild_id, value,)
                )
            else:
                self.cur.execute(
                    "SELECT * FROM MOVIENIGHT WHERE guild_id = ? AND link = ?;", (guild_id, value,)
                )

            result = self.cur.fetchone()
            self.con.close()

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
            self.Connect()
            self.cur.execute(
                "DELETE FROM MOVIENIGHT WHERE guild_id = ? AND id = ?;", (guild_id, value,)
            )
            self.con.commit()
            self.con.close()

        except Error as e:
            log.error(f"[%s] {e}", __class__.__name__)
        except Exception as e:
            log.error(f"[%s] {e}", __class__.__name__)


    def Commit(self):
        self.con.commit()

    def Close(self):
        self.con.close()


# # check if table exists
# print('Check if STUDENT table exists in the database:')
# listOfTables = cur.execute(
#   """SELECT tableName FROM sqlite_master WHERE type='table'
#   AND tableName='STUDENT'; """).fetchall()
 
# if listOfTables == []:
#     print('Table not found!')
# else:
#     print('Table found!')
 
# # check if table exists
# print('Check if TEACHER table exists in the database:')
# listOfTables = cur.execute(
#   """SELECT name FROM sqlite_master WHERE type='table'
#   AND name='TEACHER'; """).fetchall()
 
# if listOfTables == []:
#     print('Table not found!')
# else:
#     print('Table found!')
 
# # commit changes
# con.commit()
 
# # terminate the connection
# con.close()
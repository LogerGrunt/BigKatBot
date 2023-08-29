import os
import nextcord
from nextcord.ext import commands
import bot_token
import logging
from logging.handlers import RotatingFileHandler
import dbwrapper

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

log_handler = RotatingFileHandler('logs/bot_logs.log', mode='a', maxBytes=5*1024*1024*20, backupCount=2, encoding=None, delay=0) #100MB
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.WARNING)

log = logging.getLogger('root')
log.setLevel(logging.WARNING)
log.addHandler(log_handler) #print to file
log.addHandler(logging.StreamHandler()) #print to console

"""
Define bot, command prefix, disable native help command, and make commands
not case sensitive
Set command prefix
"""
prefix = "bk!"
intents = nextcord.Intents.all()
bot = commands.Bot(
    command_prefix=prefix, help_command=None, case_insensitive=True, intents=intents
)


"""
Load cog extensions for bot
"""
for filename in os.listdir("./cogs"):
   if filename.endswith(".py"):
       bot.load_extension(f"cogs.{filename[:0-3]}")


#if you get a build error uninstall distro_info
#sudo apt remove python3-distro-info


@bot.event
async def on_ready():
    """
    Simple, on-ready event that logs to console when bot is connected and ready
    """
    dbwrapper.DiscordDB().CheckTables()
    log.warning(f"[%s] {bot.user.name} is connected and ready!", "MAIN")

if __name__ == "__main__":
    bot.run(bot_token.TOKEN)

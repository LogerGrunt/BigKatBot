import os
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
import bot_token
import logging
from logging.handlers import RotatingFileHandler
import dbwrapper
import event_utils
from aiohttp import connector

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

log_handler = RotatingFileHandler('logs/bot_logs.log', mode='a', maxBytes=5*1024*1024*20, backupCount=2, encoding=None, delay=0) #100MB
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.WARNING)

log = logging.getLogger('root')
log.setLevel(logging.WARNING)
log.addHandler(log_handler) #print to file

console = logging.StreamHandler()                                               
console.setLevel(logging.WARNING)                                                  
console.setFormatter(log_formatter)  
log.addHandler(console) #print to console

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
eventObj = event_utils.EventUtils(bot)

"""
Load cog extensions for bot
"""
for filename in os.listdir("./cogs"):
   if filename.endswith(".py"):
       #log.warning(f"[%s] cogs.{filename[:0-3]}", "MAIN")
       bot.load_extension(f"cogs.{filename[:0-3]}")


#if you get a build error uninstall distro_info
#sudo apt remove python3-distro-info

@bot.event
async def on_ready():
    """
    Simple, on-ready event that logs to console when bot is connected and ready
    """
    with dbwrapper.DiscordDB() as dbobj:
        dbobj.CheckTables()

    #get the updated events and store them in DB
    #make sure to update the bot object with the updated cache
    eventObj.setBot(bot)
    await eventObj.update_events_db()

    log.warning(f"[%s] {bot.user.name} is connected and ready!", "MAIN")

@bot.event
async def on_command_error(ctx:commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        command = ctx.invoked_with
        await ctx.send(f"The command [`{command}`] you have executed is not found.  Please use `{ctx.prefix}help`")
    if isinstance(error, commands.MissingPermissions):
        command = ctx.invoked_with
        await ctx.send(f"You don't have permission for that command.")

@bot.event
async def on_guild_scheduled_event_create(event:nextcord.ScheduledEvent):
    eventObj.add_event(event)

@bot.event
async def on_guild_scheduled_event_update(before_event:nextcord.ScheduledEvent, after_event:nextcord.ScheduledEvent):
   await eventObj.update_guild_events(after_event)

@bot.event
async def on_guild_scheduled_event_delete(event:nextcord.ScheduledEvent):
    eventObj.remove_event(event)

if __name__ == "__main__":
    try:
        bot.run(bot_token.TOKEN)
    except connector.ClientConnectorError:
        pass


#while True:
#    try:                
#        bot.run(botToken)
#    except Exception as e:
#        print(f'Restarting in 10s\nError: {e}')
#        sleep(10)
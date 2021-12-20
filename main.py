import os
import nextcord
import logging
from nextcord.ext import commands
import keep_alive
import dbwrapper

test = dbwrapper.DiscordDB()
test.Connect()
test.setDB("A","B")
test.Close()

"""
Basic logging config
"""
logging.basicConfig(format="%(message)s", level="WARNING")
log = logging.getLogger("root")

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


@bot.event
async def on_ready():
    """
    Simple, on-ready event that logs to console when bot is connected and ready
    """
    log.warning(f"{bot.user.name} is connected and ready!")


if __name__ == "__main__":
    # Setup Flask webserver for 24/7 uptime with Uptimerobot pinging every 20 minutes
    keep_alive.keep_alive()
    my_secret = os.environ.get("TOKEN", None)
    bot.run(my_secret)

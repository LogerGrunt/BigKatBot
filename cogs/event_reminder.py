import nextcord
from nextcord.ext import tasks, commands
from nextcord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import dbwrapper
import logging
import event_utils
from datetime import datetime, timezone
import time

log = logging.getLogger('root')

class EventReminder(commands.Cog):
    def __init__(self, bot):
        self.bot: nextcord.Client = bot
        #self.EventChecks.start()

    def cog_unload(self):
        self.EventChecks.cancel()

    @tasks.loop(minutes=1)
    async def EventChecks(self):
        #for guild in self.bot.guilds:
        #    log.warning(f"[%s] {guild.name} | {guild.id}", "EventReminder")
        with dbwrapper.DiscordDB() as dbobj:
            result = dbobj.Events_List()
            if result is not None:
                for row in result:

                    #https://stackoverflow.com/questions/12281975/convert-timestamps-with-offset-to-datetime-obj-using-strptime
                    #https://ehmatthes.com/blog/faster_than_strptime/#using-datetimefromisoformat
                    start_time = datetime.fromisoformat(row[3])
                    #print("type1", start_time.month, start_time.day, start_time.year, start_time.hour, start_time.minute, start_time.tzinfo)

                    # Convert to Unix timestamp
                    #https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes
                    d1_ts = time.mktime(datetime.now(timezone.utc).timetuple())
                    d2_ts = time.mktime(start_time.timetuple())

                    # They are now in seconds, subtract and then divide by 60 to get minutes.
                    print('x', int(d2_ts-d1_ts) / 60)
                    print('end')

    #@EventChecks.before_loop
    #async def before_EventChecks(self):
    #    await self.bot.wait_until_ready()

    @commands.command(name="event-start")
    async def eventstart_command(self, ctx:commands.Context):
        self.EventChecks.start()

    @commands.command(name="event-stop")
    async def eventstop_command(self, ctx:commands.Context):
        self.EventChecks.cancel()

    #@client.command()
    #async def rp(ctx):
    #    channel = ctx.guild.get_channel(int(CHANNEL_ID)) # voice_channel
    #    now = datetime.now(timezone.utc) + timedelta(seconds=10)
    #    await ctx.guild.create_scheduled_event(
    #        name="roleplay-sessions",
    #        channel = channel,
    #        privacy_level = nextcord.ScheduledEventPrivacyLevel.guild_only, # optional
    #        start_time = now,
    #        description = 'lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et.',
    #        entity_type = nextcord.ScheduledEventEntityType.voice
    #        )
        
def setup(bot:nextcord.Client):
    bot.add_cog(EventReminder(bot))
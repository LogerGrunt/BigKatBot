import nextcord
from nextcord.ext import tasks, commands
from nextcord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import dbwrapper
import logging

log = logging.getLogger('root')

class EventReminder(commands.Cog):
    def __init__(self, bot):
        self.bot: nextcord.Client = bot
        #self.EventChecks.start()

    def cog_unload(self):
        self.EventChecks.cancel()

    @tasks.loop(seconds=5.0)
    async def EventChecks(self):
        for guild in self.bot.guilds:
            log.warning(f"[%s] {guild.name} | {guild.id}", "EventReminder")

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
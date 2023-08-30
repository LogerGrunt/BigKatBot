import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import dbwrapper
import logging

log = logging.getLogger('root')

class ConfigureChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Configure command for updating announcement channel
    """

    @commands.command(name="set-announce")
    @commands.has_permissions(manage_channels=True)
    async def announce_config(self, ctx, channel):

        """
        Takes a channel ID as an arguement (906217502554599425)
        example:  !set-announce 906217502554599425

        Includes a permission check so that only users with the
        "manage_channels" permission can use this command.

        All messages and commands are cleared after 10 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        channel = channel.replace("[", "").replace("]", "")  # if ID is wrapped in []
        channel = channel.replace("<#", "").replace(">", "")  # if <#channelid> remove <# and >
        channel = self.bot.get_channel(int(channel))
        if channel is None:
            await ctx.send("There is no channel with that ID.", delete_after=10)
        else:
            channel_id = str(channel.id)
            channel_name = f"<#{channel_id}>"

            #log.warning(f"Debug1: [%s] {ctx.message.guild.id}")
            #log.warning(f"Debug2: [%s] {ctx.guild.id}")
            #ctx.message.guild.id
            #ctx.guild.id
            #guild = discord.utils.get(bot.guilds, id=378473289473829)
            #guild = await client.get_guild(id)
            # for guild in bot.guilds:
            #     print(guild.id)

            with dbwrapper.DiscordDB() as dbobj:
                dbobj.SetChannel(ctx.message.guild.id, "announce_channel", channel_id)

            await ctx.send(
                f"Announcements channel has been updated to:  {channel_name} (ID: {channel_id})",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)

    @announce_config.error
    async def announce_config_error(self, ctx, error):
        """
        Error check, if command user is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 10 seconds to keep
        channels clear of unnecessary error messages.
        """

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a \#channellink",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)

def setup(bot):
    bot.add_cog(ConfigureChannels(bot))

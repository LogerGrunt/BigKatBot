import nextcord
from replit import db
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions


class ConfigureChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prevent error if DB missing key
    def getDB(self, key):
        if not key in db.keys():
            return None
        else:
            return db[key]

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

        All messages and commands are cleared after 30 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        channel = channel.replace("[", "").replace("]", "")  # if ID is wrapped in []
        channel = self.bot.get_channel(int(channel))
        if channel is None:
            await ctx.send("There is no channel with that ID.", delete_after=30)
        else:
            channel_id = str(channel.id)
            channel_name = f"<#{channel_id}>"

            if self.getDB("announce_channel") == channel_id:
                await ctx.send(
                    f"{channel_name} is already your set Announcements channel.",
                    delete_after=30,
                )

            else:
                db["announce_channel"] = channel_id
                await ctx.send(
                    f"Announcements channel has been updated to:  {channel_name} (ID: {channel_id})",
                    delete_after=30,
                )
            await ctx.message.delete(delay=30)

    @announce_config.error
    async def announce_config_error(self, error, ctx):
        """
        Error check, if command user is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)

    """
    Configure command for updating member join announcement channel
    """

    @commands.command(name="set-join")
    @commands.has_permissions(manage_channels=True)
    async def join_config(self, ctx, channel):
        """
        Takes a channel ID as an arguement (906217502554599425)
        example:  !set  906217502554599425

        Includes a permission check so that only users with the
        "manage_channels" permission can use this command.

        All messages and commands are cleared after 30 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        channel = channel.replace("[", "").replace("]", "")  # if ID is wrapped in []
        channel = self.bot.get_channel(int(channel))
        if channel is None:
            await ctx.send("There is no channel with that ID.", delete_after=30)
        else:
            channel_id = str(channel.id)
            channel_name = f"<#{channel_id}>"

        if self.getDB("member_join_channel") == channel_id:
            await ctx.send(
                f"{channel_name} is already your set Member Join alerts channel.",
                delete_after=30,
            )
        else:
            db["member_join_channel"] = channel_id

            await ctx.send(
                f"Member join alerts channel has been updated to:  {channel_name} (ID: {channel_id})",
                delete_after=30,
            )
        await ctx.message.delete(delay=30)

    @join_config.error
    async def join_config_error(self, error, ctx):
        """
        Error check, if command user is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """
        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)

    """
    Command for updating member leave announcement channel
    """

    @commands.command(name="set-leave")
    @commands.has_permissions(manage_channels=True)
    async def leave_config(self, ctx, channel):
        """
        Takes a channel ID as an arguement (906217502554599425)
        example:  !set  906217502554599425

        Includes a permission check so that only users with the
        "manage_channels" permission can use this command.

        All messages and commands are cleared after 30 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        channel = channel.replace("[", "").replace("]", "")  # if ID is wrapped in []
        channel = self.bot.get_channel(int(channel))
        if channel is None:
            await ctx.send("There is no channel with that ID.", delete_after=30)
        else:
            channel_id = str(channel.id)
            channel_name = f"<#{channel_id}>"

        if self.getDB("member_leave_channel") == channel_id:
            await ctx.send(
                f"{channel_name} is already your set Member leave alerts channel.",
                delete_after=30,
            )
        else:
            db["member_leave_channel"] = channel_id
            await ctx.send(
                f"Member leave alerts channel has been updated to:  {channel_name} (ID: {channel_id})",
                delete_after=30,
            )
        await ctx.message.delete(delay=30)

    @leave_config.error
    async def leave_config_error(self, error, ctx):
        """
        Error check, if command user is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)

    """
    Command for updating bot channel
    """

    @commands.command(name="set-bot")
    @commands.has_permissions(manage_channels=True)
    async def botchannel_config(self, ctx, channel):
        """
        Takes a channel ID as an arguement (906217502554599425)
        example:  !set  906217502554599425

        Includes a permission check so that only users with the
        "manage_channels" permission can use this command.

        All messages and commands are cleared after 30 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        channel = channel.replace("[", "").replace("]", "")  # if ID is wrapped in []
        channel = self.bot.get_channel(int(channel))
        if channel is None:
            await ctx.send("There is no channel with that ID.", delete_after=30)
        else:
            channel_id = str(channel.id)
            channel_name = f"<#{channel_id}>"

        if self.getDB("bot_channel") == channel_id:
            await ctx.send(
                f"{channel_name} is already your bot channel.",
                delete_after=30,
            )
        else:
            db["bot_channel"] = channel_id
            await ctx.send(
                f"Bot channel has been updated to:  {channel_name} (ID: {channel_id})",
                delete_after=30,
            )
        await ctx.message.delete(delay=30)

    @leave_config.error
    async def botchannel_config_error(self, error, ctx):
        """
        Error check, if command user is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)

    """
    Command for updating reaction role channel
    """

    @commands.command(name="set-reactionrole")
    @commands.has_permissions(manage_channels=True)
    async def reactionrolechannel_config(self, ctx, channel):
        """
        Takes a channel ID as an arguement (906217502554599425)
        example:  !set  906217502554599425

        Includes a permission check so that only users with the
        "manage_channels" permission can use this command.

        All messages and commands are cleared after 30 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        channel = channel.replace("[", "").replace("]", "")  # if ID is wrapped in []
        channel = self.bot.get_channel(int(channel))
        if channel is None:
            await ctx.send("There is no channel with that ID.", delete_after=30)
        else:
            channel_id = str(channel.id)
            channel_name = f"<#{channel_id}>"

        if self.getDB("reactionrole_channel") == channel_id:
            await ctx.send(
                f"{channel_name} is already your reaction role channel.",
                delete_after=30,
            )
        else:
            db["reactionrole_channel"] = channel_id
            await ctx.send(
                f"Reaction role channel has been updated to:  {channel_name} (ID: {channel_id})",
                delete_after=30,
            )
        await ctx.message.delete(delay=30)

    @leave_config.error
    async def reactionrolechannel_config_error(self, error, ctx):
        """
        Error check, if command user is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)


def setup(bot):
    bot.add_cog(ConfigureChannels(bot))

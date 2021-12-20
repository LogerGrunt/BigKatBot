import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
import dbwrapper


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

            dbobj = dbwrapper.DiscordDB()
            dbobj.Connect()
            db_result = str(dbobj.getDB("announce_channel"))

            if db_result == channel_id:
                await ctx.send(
                    f"{channel_name} is already your set Announcements channel.",
                    delete_after=30,
                )

            else:
                dbobj.setDB("announce_channel", channel_id)

                await ctx.send(
                    f"Announcements channel has been updated to:  {channel_name} (ID: {channel_id})",
                    delete_after=30,
                )
            await ctx.message.delete(delay=30)

            dbobj.Close()



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

            dbobj = dbwrapper.DiscordDB()
            dbobj.Connect()
            db_result = str(dbobj.getDB("member_join_channel"))

            if db_result == channel_id:
                await ctx.send(
                    f"{channel_name} is already your set Member Join alerts channel.",
                    delete_after=30,
                )
            else:
                dbobj.setDB("member_join_channel", channel_id)

                await ctx.send(
                    f"Member join alerts channel has been updated to:  {channel_name} (ID: {channel_id})",
                    delete_after=30,
                )
            await ctx.message.delete(delay=30)

            dbobj.Close()

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

            dbobj = dbwrapper.DiscordDB()
            dbobj.Connect()
            db_result = str(dbobj.getDB("member_leave_channel"))

            if db_result == channel_id:
                await ctx.send(
                    f"{channel_name} is already your set Member leave alerts channel.",
                    delete_after=30,
                )
            else:
                dbobj.setDB("member_leave_channel", channel_id)

                await ctx.send(
                    f"Member leave alerts channel has been updated to:  {channel_name} (ID: {channel_id})",
                    delete_after=30,
                )
            await ctx.message.delete(delay=30)

            dbobj.Close()

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

            dbobj = dbwrapper.DiscordDB()
            dbobj.Connect()
            db_result = str(dbobj.getDB("bot_channel"))

            if db_result == channel_id:
                await ctx.send(
                    f"{channel_name} is already your bot channel.",
                    delete_after=30,
                )
            else:
                dbobj.setDB("bot_channel", channel_id)

                await ctx.send(
                    f"Bot channel has been updated to:  {channel_name} (ID: {channel_id})",
                    delete_after=30,
                )
        await ctx.message.delete(delay=30)

        dbobj.Close()

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

            dbobj = dbwrapper.DiscordDB()
            dbobj.Connect()
            db_result = str(dbobj.getDB("reactionrole_channel"))

            if db_result == channel_id:
                await ctx.send(
                    f"{channel_name} is already your reaction role channel.",
                    delete_after=30,
                )
            else:
                dbobj.setDB("reactionrole_channel", channel_id)

                await ctx.send(
                    f"Reaction role channel has been updated to:  {channel_name} (ID: {channel_id})",
                    delete_after=30,
                )
            await ctx.message.delete(delay=30)

            dbobj.Close()

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

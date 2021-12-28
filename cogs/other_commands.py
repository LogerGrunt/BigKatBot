import os
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import *
import dbwrapper
import traceback
import sys
import emoji as emojiLib
from datetime import datetime
import pytz


class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getWelcomeMessage(self):
        with open("./messages/welcome.txt") as f:
            message = f.read()
        return message

    @commands.command(name="spank")
    async def spank_command(self, ctx, member: nextcord.Member):
        guild = ctx.guild
        emoji = nextcord.utils.get(guild.emojis, name="spank_smirk")
        embed = nextcord.Embed(
            title="Incoming Spank!",
            description=f"**:wave: {ctx.author.mention} gives {member.mention} a good spank! {emoji}:heart:**",
            color=0x40A923,
        )
        await ctx.send(embed=embed)

    @commands.command(name="welcome")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def welcome_command(self, ctx, member: nextcord.Member):
        """
        Welcome command will remove the Visitors role and replace it with the
        Members role for the targetted member.  It will also send a Welcome message (messages/welcome.txt)
        to the member_join_channel (retrieved from DB)

        Member argument can be an ID, discord name, or mention
        """
        owner = member.guild.get_member(int(os.environ.get("ADMINID", 0)))  # your ID

        dbobj = dbwrapper.DiscordDB()
        dbobj.Connect()
        channel_id = int(dbobj.getDB("member_join_channel"))

        if channel_id is None:
            await owner.send(
                "(welcome_command) There was an error retrieving the channel ID (member_join_channel) from DB"
            )
        else:
            member_ch = self.bot.get_channel(channel_id)
            guild = ctx.guild
            old_role = nextcord.utils.get(guild.roles, name="Visitors")
            new_role = nextcord.utils.get(guild.roles, name="FC Members")

            botchannel_id = str(dbobj.getDB("bot_channel"))
            reactionrole_ch_id = str(dbobj.getDB("reactionrole_channel"))

            if botchannel_id is None or reactionrole_ch_id is None:
                await owner.send(
                    "(welcome_command) There was an error retrieving the channel ID (botchannel_id) or (reactionrole_ch_id)  from DB"
                )

            else:
                message = self.getWelcomeMessage()
                message = (
                    message.replace("member.mention", member.mention)
                    .replace("botchannel_id", botchannel_id)
                    .replace("reactionrole_ch_id", reactionrole_ch_id)
                )

                """
              Check member for old role.  If exists, remove old role and add new role,
              then send welcome message to member join channel
              """
                if old_role in member.roles:
                    await member.remove_roles(old_role)
                    await member.add_roles(new_role)
                    await member.send(message)  # send a Direct Message
                    await member_ch.send(
                        message
                    )  # send a message to the member_join_channel channel

        dbobj.Close()
        await ctx.message.delete(delay=5)

    @welcome_command.error
    async def welcome_command_error(self, ctx, error):
        """
        Error check, if command user or bot is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(
                "The bot is missing 'Manage Roles' permission.", delete_after=30
            )
            await ctx.message.delete(delay=30)
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(
                "Ignoring exception in command {}:".format(ctx.invoked_with),
                file=sys.stderr,
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

    # add event with a reaction
    @commands.command(name="event")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True, add_reactions=True)
    async def event_command(self, ctx, *, message=None):

        if message is None:
            await ctx.send(
                "Sorry. There is no message to process.",
                delete_after=30,
            )
        else:
            embed = nextcord.Embed(
                title="[Custom Event]",
                description='\n',
                color=0x40A923,
            )
            embed.add_field(name="Author:", value=ctx.author.mention, inline=False)

            now = datetime.now(
                pytz.timezone("America/New_York")
            )  # current date and time / Eastern
            created_on = now.strftime("%m/%d/%Y, %-I:%M:%S %p %Z")

            embed.add_field(name="Start Date/Time:", value=created_on+'\n', inline=False)
            #embed.add_field(name = chr(173), value = chr(173)) #add empty space

            embed.add_field(name="Message:", value=message, inline=False)
            newMessage = await ctx.send(embed=embed)

            reactions = ["white_check_mark"]
            # reactions = ["white_check_mark", "stop_sign", "no_entry_sign", "spanksmirk"]
            guild = ctx.guild

            for emoji in reactions:
                # check for unicode first
                emojiChk = emojiLib.emojize(''.join(":"+emoji+":"), use_aliases=True)
                
                if emojiChk is not None and emojiLib.is_emoji(emojiChk):
                    await newMessage.add_reaction(emojiChk)
                    # msg.add_reaction('✓') await msg.add_reaction('❌')
                else:
                    emojiObj = nextcord.utils.get(guild.emojis, name=emoji)

                    if emojiObj is not None:
                        await newMessage.add_reaction(emojiObj)

            await ctx.message.delete(delay=5)

    async def event_command_error(self, ctx, error):
        """
        Error check, if command user or bot is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        """

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        if isinstance(error, MissingPermissions):
            await ctx.send(
                "Sorry. You do not have permission to use that command.",
                delete_after=30,
            )
            await ctx.message.delete(delay=30)
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(
                "The bot is missing 'Manage Roles' permission.", delete_after=30
            )
            await ctx.message.delete(delay=30)
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(
                "Ignoring exception in command {}:".format(ctx.invoked_with),
                file=sys.stderr,
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot):
    bot.add_cog(OtherCommands(bot))

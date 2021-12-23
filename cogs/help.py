import nextcord
from nextcord.ext import commands
import traceback
import sys

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):

        embed = nextcord.Embed(
            title=f"About {self.bot.user.name}",
            description=f"""**General Features**:
            **Member Leave Alerts**
            Custom message is posted to the configured channel when a member has left or been kicked from the server.

            **Admin Features**:
            **Emoji Pin**
            React to a message with :pushpin: emoji and the bot will pin that message to the channel.

            **Emoji Announce**
            React to a message with :mega: emoji and the bot will announce that message to the configured announcement channel.

            """,
        )
        embed.add_field(
            name="General Commands",
            value=f"""
                        `{ctx.prefix}spank @member`
                        Spanks a member with a bot displayed message.
                        """,
            inline=False,
        )

        embed.add_field(
            name="Admin Commands",
            value=f"""
                        `{ctx.prefix}welcome @member`
                        Removes Visitors Role and grants Member Role. Displays a welcome message.

                        `{ctx.prefix}set-announce [channelID]`
                        Set the general announcements channel by ID

                        `{ctx.prefix}set-bot [channelID]`
                        Set the general bot channel by ID

                        `{ctx.prefix}set-reactionrole [channelID]`
                        Set the general reaction role channel by ID
                                              
                        `{ctx.prefix}set-join [channelID]`
                        Set member join announcemnets by ID

                        `{ctx.prefix}set-leave [channelID]`
                         Set member leave announcements by ID
                        """,
            inline=False,
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommand(bot))

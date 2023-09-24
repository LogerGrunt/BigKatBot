import nextcord
from nextcord.ext import commands
import textwrap
import logging

log = logging.getLogger('root')

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: nextcord.Client = bot

    @commands.command(name="help")
    async def help_command(self, ctx:commands.Context):

        embed = nextcord.Embed(
            title="BigKatBot Help",
        )
    
        embed.add_field(
            name=":information_source:  IMPORTANT NOTE:",
            value=textwrap.dedent(f"""
                Please use quotes when passing long text strings as parameters for commands.
                In addition please use spaces to separate multiple passing parameters.
                
                :white_check_mark: **EXAMPLE**: `bk!movie-add "A Big Red Apple" MovielinkHere`
                :white_check_mark:  **EXAMPLE**: `bk!movie-find "A Big Red Apple"`
                :x: **DO NOT DO THIS**:  `bk!movie-find A Big Red Apple`
                \u200b                              
            """),
            inline=False,
        )

        embed.add_field(
            name=":hammer:  Admin Commands",
            value=textwrap.dedent(f"""
                `{ctx.prefix}set-announce channelid or channelmention`
                Sets the announcement channel for the event tracking notifications.
                \u200b
            """),
            inline=False,
        )
    
        embed.add_field(
            name=":calendar:  Event Tracking:",
            value=textwrap.dedent(f"""
                Event tracking stuff.
                \u200b                                  
            """),
            inline=False,
        )
        
        embed.add_field(
            name=":cinema:  Movie Night Commands",
            value=textwrap.dedent(f"""
                `{ctx.prefix}movie-add "movie title" link/url` or `{ctx.prefix}movie-add link/url`
                Adds a movie to the database.
                
                `{ctx.prefix}movie-remove MovieID or link/url`
                :warning:Admin Only: Removes a movie from the database.
                
                `{ctx.prefix}movie-random`
                Randomly selects a movie from the database.

                `{ctx.prefix}movie-watched MovieID or link/url`
                :warning:Admin Only: Sets a movie as watched in the database and prevents it from being selected with movie-random.
            """),
            inline=False,
        )
        #embd values have a max of 1024 characters, so you have to add new ones using the bold tag to get rid of the name variable
        embed.add_field(
            name="** **",
            value=textwrap.dedent(f"""
                `{ctx.prefix}movie-fame MovieID or link/url`
                :warning:Admin Only: Toggles the fame status true/false of a movie in the database.
                                        
                `{ctx.prefix}movie-info MovieID or link/url`
                Returns information on a movie from the database.

                `{ctx.prefix}movie-find searchtext`
                Returns all movies in the database that match the search criteria provided.
                \u200b
            """),
            inline=False,
        )

        embed.add_field(
            name=":hammer:  Admin Commands",
            value=textwrap.dedent(f"""
                `{ctx.prefix}set-announce channelid or channelmention`
                Sets the announcement channel for the event tracking notifications.
                \u200b
            """),
            inline=False,
        )
        await ctx.send(embed=embed)


def setup(bot:nextcord.Client):
    bot.add_cog(HelpCommand(bot))

import nextcord
from nextcord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):

        embed = nextcord.Embed(
            title=f"About {self.bot.user.name}",
            description=f"""**:calendar:  Event Tracking:**
            Event tracking stuff.

            """,
        )
        embed.add_field(
            name=":cinema:  Movie Night Commands",
            value=f"""
                        `{ctx.prefix}movie-add link/url`
                        Adds a movie to the database.
                        
                        `{ctx.prefix}movie-remove MovieID or link/url`
                        :warning:Admin Only: Removes a movie from the database.
                        
                        `{ctx.prefix}movie-random`
                        Randomly selects a movie from the database.

                        `{ctx.prefix}movie-watched MovieID or link/url`
                        :warning:Admin Only: Sets a movie as watched in the database and prevents it from being selected with movie-random.

                        """,
            inline=False,
        )
        #embd values have a max of 1024 characters, so you have to add new ones using the bold tag to get rid of the name variable
        embed.add_field(
            name="** **",
            value=f"""
                        `{ctx.prefix}movie-fame MovieID or link/url`
                        :warning:Admin Only: Toggles the fame status true/false of a movie in the database.
                                              
                        `{ctx.prefix}movie-info MovieID or link/url`
                        Returns information on a movie from the database.

                        `{ctx.prefix}movie-find searchtext`
                        Returns all movies in the database that match the search criteria provided.

                        """,
            inline=False,
        )
        embed.add_field(
            name=":hammer:  Admin Commands",
            value=f"""
                        `{ctx.prefix}set-announce channelid or channelmention`
                        Sets the announcement channel for the event tracking notifications.

                        """,
            inline=False,
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommand(bot))

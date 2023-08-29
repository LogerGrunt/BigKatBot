import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import dbwrapper
import logging

log = logging.getLogger('root')

class MovieNight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()
        
    @commands.command(name="movie-add")
    async def movie_add(self, ctx, movielink):

        """
        Takes a link
        example:  !movie-add https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14

        All messages and commands are cleared after 10 seconds to keep
        channels clear of unnecessary commands and notification messages
        """

        if movielink is None:
            await ctx.send("You must provide a link.", delete_after=10)
        elif self.is_integer(movielink) is True:
            await ctx.send("You must provide a link not an integer.", delete_after=10)
        else:

            result = dbwrapper.DiscordDB().MovieNight_Get(ctx.message.guild.id, movielink)
            if result is not None:
                await ctx.send(
                    f":warning: Movie already added as MovieID: {result[0]}",
                )
                await ctx.message.delete(delay=3)
            else:
                movieID=dbwrapper.DiscordDB().MovieNight_Add(ctx.message.guild.id, movielink)

                await ctx.send(
                    f"MovieID: {movieID}\nMovie Added: {movielink}\n\n",
                )
                await ctx.message.delete(delay=3)
            
    @movie_add.error
    async def movie_add_error(self, ctx, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a link!",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)


    @commands.command(name="movie-remove")
    async def movie_remove(self, ctx, movielink):

        """
        Takes a link or movieID
        example:  !movie-remove https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14
        example:  !movie-remove 12

        All messages and commands are cleared after 10 seconds to keep
        channels clear of unnecessary commands and notification messages
        """

        if movielink is None:
            await ctx.send("You must provide a MovieID or link.", delete_after=10)
        else:
            result = dbwrapper.DiscordDB().MovieNight_Get(ctx.message.guild.id, movielink)
            if result is not None:
                dbwrapper.DiscordDB().MovieNight_Remove(ctx.message.guild.id, result[0])
                await ctx.send(
                    f":no_entry_sign:  MovieID: {result[0]} has been removed!\nMovie: {result[2]}",
                )
                await ctx.message.delete(delay=3)
            else:
                await ctx.send(
                    "No movie with the MovieID or link was found!",
                    delete_after=10,
                )
                await ctx.message.delete(delay=3)
            
    @movie_remove.error
    async def movie_remove_error(self, ctx, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a MovieID or link",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)


def setup(bot):
    bot.add_cog(MovieNight(bot))

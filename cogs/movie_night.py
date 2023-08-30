import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import dbwrapper
import logging
import textwrap
import validators

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
        elif validators.url(movielink) is False:
            await ctx.send("You must provide a valid url web link.", delete_after=10)
        else:
            with dbwrapper.DiscordDB() as dbobj:
                result = dbobj.MovieNight_Get(ctx.message.guild.id, movielink)
                if result is not None:
                    await ctx.send(
                        f":warning: Movie already added as MovieID: {result[0]}",
                    )
                    await ctx.message.delete(delay=3)
                else:
                    movieID=dbobj.MovieNight_Add(ctx.message.guild.id, movielink)

                    response = f"""
                    :white_check_mark::white_check_mark::white_check_mark: **MOVIE ADDED**
                    
                    **User**: {ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>
                    
                    **MovieID**: {movieID}
                    **Movie**: {movielink}
                    """
                    await ctx.send(textwrap.dedent(response))
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
        elif self.is_integer(movielink) is False and validators.url(movielink) is False:
            await ctx.send("You must provide a valid url web link.", delete_after=10)
        else:
            with dbwrapper.DiscordDB() as dbobj:
                result = dbobj.MovieNight_Get(ctx.message.guild.id, movielink)
                if result is not None:
                    dbobj.MovieNight_Remove(ctx.message.guild.id, result[0])

                    response = f"""
                    :no_entry_sign::no_entry_sign::no_entry_sign: **MOVIE REMOVED**

                    **User**: {ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>
                    
                    **MovieID**:  {result[0]}
                    **Movie**: {result[2]}
                    """
                    await ctx.send(textwrap.dedent(response))
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

    @commands.command(name="movie-random")
    async def movie_random(self, ctx):

        """
        All messages and commands are cleared after 10 seconds to keep
        channels clear of unnecessary commands and notification messages
        """
        with dbwrapper.DiscordDB() as dbobj:
            result = dbobj.MovieNight_Random(ctx.message.guild.id)
            if result is not None:
                response = f"""
                :game_die::game_die::game_die:  **RANDOM MOVIE**

                **User**: {ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>
                
                **MovieID**:  {result[0]}
                **Movie**: {result[2]}
                """
                await ctx.send(textwrap.dedent(response))
            else:
                await ctx.send(
                    "There are no entries in the database!",
                    delete_after=10,
                )
                await ctx.message.delete(delay=3)
            
    @movie_random.error
    async def movie_random_error(self, ctx, error):
        await ctx.send(
            "Sorry. There was an error retrieving a random.",
            delete_after=10,
        )
        await ctx.message.delete(delay=10)
        log.error(f"[%s] {error}", __class__.__name__)


def setup(bot):
    bot.add_cog(MovieNight(bot))

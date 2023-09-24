import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument
import dbwrapper
import logging
import textwrap
import validators
import requests
from bs4 import BeautifulSoup

log = logging.getLogger('root')

class MovieNight(commands.Cog):
    def __init__(self, bot):
        self.bot: nextcord.Client = bot

    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    def bool_string(self, n):
        boolChk = ':x:'
        if n == 1:
            boolChk = ':white_check_mark:'

        return boolChk

    @commands.command(name="movie-add")
    async def movie_add(self, ctx:commands.Context, movietitle, movielink=None):
        
        """
        Takes a link
        example:  !movie-add "movie title" https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14
        example:  !movie-add https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14

        movielink=None allows the second parameter to be optional

        All messages and commands are cleared after 10 seconds to keep
        channels clear of unnecessary commands and notification messages
        """

        """ Check the first parameter, it can be a title or a link.  If it's a link then lets grab the webpage title."""
        if validators.url(movietitle) is True and movielink is None:
            response = requests.get(movietitle)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string

            if title is not None:
                movielink = movietitle
                movietitle = title

        if movietitle is None or movielink is None:
            await ctx.send("""Invalid Syntax: `bk!movie-add link` or `bk!movie-add "movie title" link`""", delete_after=10)
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
                    movieID=dbobj.MovieNight_Add(ctx.message.guild.id, movietitle, movielink)

                    embed = nextcord.Embed(
                        title=f":white_check_mark::white_check_mark::white_check_mark: **MOVIE ADDED**",
                        description="** **",                        
                    )
                    embed.add_field(
                        name="User",
                        value=f"{ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>",
                        inline=False,
                    )
                    embed.add_field(
                        name="MovieID",
                        value=f"{movieID}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Title",
                        value=f"{movietitle}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Movie",
                        value=f"<{movielink}>",
                        inline=False,
                    )        
                    await ctx.send(embed=embed)
                    await ctx.message.delete(delay=3)


    @movie_add.error
    async def movie_add_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                """Invalid Syntax: `bk!movie-add link` or `bk!movie-add "movie title" link`""",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)

    @commands.command(name="movie-remove")
    @commands.has_permissions(manage_channels=True)
    async def movie_remove(self, ctx:commands.Context, movielink):

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

                    embed = nextcord.Embed(
                        title=f":x::x::x: **MOVIE REMOVED**",
                        description="** **",                 
                    )
                    embed.add_field(
                        name="User",
                        value=f"{ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>",
                        inline=False,
                    )
                    embed.add_field(
                        name="MovieID",
                        value=f"{result[0]}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Title",
                        value=f"{result[2]}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Movie",
                        value=f"<{result[3]}>",
                        inline=False,
                    )  

                    await ctx.send(embed=embed)
                    await ctx.message.delete(delay=3)
                else:
                    await ctx.send(
                        "No movie with the MovieID or link was found!",
                        delete_after=10,
                    )
                    await ctx.message.delete(delay=3)
            
    @movie_remove.error
    async def movie_remove_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a MovieID or link",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)

    @commands.command(name="movie-random")
    async def movie_random(self, ctx:commands.Context):

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
                **Title**: {result[2]}
                **Movie**: {result[3]}
                """
                await ctx.send(textwrap.dedent(response))
            else:
                await ctx.send(
                    "There are no entries in the database!",
                    delete_after=10,
                )
                await ctx.message.delete(delay=3)
            
    @movie_random.error
    async def movie_random_error(self, ctx:commands.Context, error):
        await ctx.send(
            "Sorry. There was an error retrieving a random.",
            delete_after=10,
        )
        await ctx.message.delete(delay=10)
        log.error(f"[%s] {error}", __class__.__name__)


    @commands.command(name="movie-watched")
    @commands.has_permissions(manage_channels=True)
    async def movie_watched(self, ctx:commands.Context, movielink):

        """
        Takes a link or movieID and toggles between true or false
        example:  !movie-watched https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14
        example:  !movie-watched 12

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
                    
                    #do the boolean toggle
                    switch = 0
                    if result[4] == 0:
                        switch = 1

                    changed = dbobj.MovieNight_Watched(ctx.message.guild.id, result[0], switch)

                    if changed is False:
                        await ctx.send("Error: No changes were done in the database.", delete_after=10)
                    else:
                        boolChk = self.bool_string(switch)

                        embed = nextcord.Embed(
                            title=f":clapper::clapper::clapper: **MOVIE WATCHED**",
                            description="** **",                 
                        )
                        embed.add_field(
                            name=f"Watched:  {boolChk}",
                            value="** **",
                            inline=False,
                        )                        
                        embed.add_field(
                            name="User",
                            value=f"{ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>",
                            inline=False,
                        )
                        embed.add_field(
                            name="MovieID",
                            value=f"{result[0]}",
                            inline=False,
                        )
                        embed.add_field(
                            name="Title",
                            value=f"{result[2]}",
                            inline=False,
                        )
                        embed.add_field(
                            name="Movie",
                            value=f"<{result[3]}>",
                            inline=False,
                        )  

                        await ctx.send(embed=embed)
                        await ctx.message.delete(delay=3)

                else:
                    await ctx.send(
                        "No movie with the MovieID or link was found!",
                        delete_after=10,
                    )
                    await ctx.message.delete(delay=3)
            
    @movie_watched.error
    async def movie_watched_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a MovieID or link",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)

    @commands.command(name="movie-fame")
    @commands.has_permissions(manage_channels=True)
    async def movie_fame(self, ctx:commands.Context, movielink):

        """
        Takes a link or movieID and toggles between true or false
        example:  !movie-fame https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14
        example:  !movie-fame 12

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
                    
                    #do the boolean toggle
                    switch = 0
                    if result[5] == 0:
                        switch = 1
        
                    changed = dbobj.MovieNight_Fame(ctx.message.guild.id, result[0], switch)

                    if changed is False:
                        await ctx.send("Error: No changes were done in the database.", delete_after=10)
                    else:
                        boolChk = self.bool_string(switch)

                        embed = nextcord.Embed(
                            title=f":trophy::trophy::trophy: **MOVIE FAME**",
                            description="** **",                 
                        )
                        embed.add_field(
                            name=f"Fame:  {boolChk}",
                            value="** **",
                            inline=False,
                        )                        
                        embed.add_field(
                            name="User",
                            value=f"{ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>",
                            inline=False,
                        )
                        embed.add_field(
                            name="MovieID",
                            value=f"{result[0]}",
                            inline=False,
                        )
                        embed.add_field(
                            name="Title",
                            value=f"{result[2]}",
                            inline=False,
                        )
                        embed.add_field(
                            name="Movie",
                            value=f"<{result[3]}>",
                            inline=False,
                        ) 

                        await ctx.send(embed=embed)
                        await ctx.message.delete(delay=3)

                else:
                    await ctx.send(
                        "No movie with the MovieID or link was found!",
                        delete_after=10,
                    )
                    await ctx.message.delete(delay=3)
            
    @movie_fame.error
    async def movie_fame_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a MovieID or link",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)

    @commands.command(name="movie-info")
    async def movie_info(self, ctx:commands.Context, movielink):

        """
        Takes a link or movieID
        example:  !movie-info https://www.youtube.com/watch?v=YhTMFDlI1l8&list=PL6dpcY8ijWKKhQ2cEuhfRU8w4eWfjdRbi&index=14
        example:  !movie-info 12

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

                    watched = self.bool_string(result[4])
                    fame = self.bool_string(result[5])

                    embed = nextcord.Embed(
                        title=f":question::question::question: **MOVIE INFO**",
                        description="** **",                 
                    )
                    embed.add_field(
                        name=f":clapper:  Watched:  {watched}",
                        value="** **",
                        inline=True,
                    )
                    embed.add_field(
                        name=f":trophy:  Fame:  {fame}",
                        value="** **",
                        inline=True,
                    )                       
                    embed.add_field(
                        name="User",
                        value=f"{ctx.author.mention} [{ctx.author.name}] <{ctx.author.display_name}>",
                        inline=False,
                    )
                    embed.add_field(
                        name="MovieID",
                        value=f"{result[0]}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Title",
                        value=f"{result[2]}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Movie",
                        value=f"<{result[3]}>",
                        inline=False,
                    ) 

                    await ctx.send(embed=embed)
                    await ctx.message.delete(delay=3)
                    
                else:
                    await ctx.send(
                        "No movie with the MovieID or link was found!",
                        delete_after=10,
                    )
                    await ctx.message.delete(delay=3)
            
    @movie_info.error
    async def movie_info_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a MovieID or link",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)


    @commands.command(name="movie-find")
    async def movie_find(self, ctx:commands.Context, findstr):

        """
        Takes a string to search if links contains the search string
        example:  !movie-find YhTMFDlI1l8

        All messages and commands are cleared after 10 seconds to keep
        channels clear of unnecessary commands and notification messages
        """

        if findstr is None:
            await ctx.send("You must provide a search text.", delete_after=10)
        else:
            with dbwrapper.DiscordDB() as dbobj:
                result = dbobj.MovieNight_Find(ctx.message.guild.id, findstr)
                if result is not None:
                    
                    response = ":mag::mag::mag:  **MOVIE FIND**\n\n"
                    for row in result:
                        response=response+textwrap.dedent(f"**MovieID**:  {row[0]}  |  **WATCHED:**  {self.bool_string(row[4])}  |  **FAME:**  {self.bool_string(row[5])}  |  **Title**:  {row[2]}  |  **Movie**:  <{row[3]}>\n\n")

                    await ctx.send(response)
                else:
                    await ctx.send(
                        "No movie with the search criteria provided was found!",
                        delete_after=10,
                    )
                    await ctx.message.delete(delay=3)
            
    @movie_find.error
    async def movie_find_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Sorry. You must provide a search text.",
                delete_after=10,
            )
            await ctx.message.delete(delay=10)
        else:
            log.error(f"[%s] {error}", __class__.__name__)


def setup(bot:nextcord.Client):
    bot.add_cog(MovieNight(bot))

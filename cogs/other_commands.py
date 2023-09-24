import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import *
import logging

log = logging.getLogger('root')

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: nextcord.Client = bot

    @commands.command(name="spank")
    async def spank_command(self, ctx:commands.Context, member: nextcord.Member):
        guild = ctx.guild
        emoji = nextcord.utils.get(guild.emojis, name="spank_smirk")
        embed = nextcord.Embed(
            title="Incoming Spank!",
            description=f"**:wave: {ctx.author.mention} gives {member.mention} a good spank! {emoji}:heart:**",
            color=0x40A923,
        )
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=3)

    @spank_command.error
    async def spank_command_error(self, ctx:commands.Context, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Correct Usage: bk!spank \@mentioned_user",
                delete_after=10,
            )
            await ctx.message.delete(delay=3)
        else:
            log.error(f"[%s] {error}", __class__.__name__)

def setup(bot:nextcord.Client):
    bot.add_cog(OtherCommands(bot))

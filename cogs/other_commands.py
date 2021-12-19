import os
import nextcord
from replit import db
from nextcord.ext import commands
from nextcord.ext.commands import *

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # replit will return an error if a DB item doesn't already exist
    def getDB(self, key):
        if key not in db.keys():
            return None
        else:
            return db[key]

    def getWelcomeMessage(self):
        with open('./messages/welcome.txt') as f:
            message = f.read()
        return message

    @commands.command(name='spank')
    async def spank_command(self, ctx, member: nextcord.Member):
        guild = ctx.guild
        emoji = nextcord.utils.get(guild.emojis, name='spank_smirk')
        embed = nextcord.Embed(title='Incoming Spank!',
                               description=f'**:wave: {ctx.author.mention} gives {member.mention} a good spank! {emoji}:heart:**', color=0x40a923)
        await ctx.send(embed=embed)

    @commands.command(name='welcome')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def welcome_command(self, ctx, member: nextcord.Member):
        '''
        Welcome command will remove the Visitors role and replace it with the
        Members role for the targetted member.  It will also send a Welcome message (messages/welcome.txt)
        to the member_join_channel (retrieved from DB)

        Member argument can be an ID, discord name, or mention
        '''
        owner = member.guild.get_member(int(os.environ['ADMINID']))  # your ID
        channel_id = int(self.getDB("member_join_channel"))
        if channel_id is None:
            await owner.send('(welcome_command) There was an error retrieving the channel ID (member_join_channel) from DB')
        else:
            member_ch = self.bot.get_channel(channel_id)
            guild = ctx.guild
            old_role = nextcord.utils.get(guild.roles, name='Visitors')
            new_role = nextcord.utils.get(guild.roles, name='FC Members')

            botchannel_id = str(self.getDB("bot_channel"))
            reactionrole_ch_id = str(self.getDB("reactionrole_channel"))

            if botchannel_id is None or reactionrole_ch_id is None:
              await owner.send('(welcome_command) There was an error retrieving the channel ID (botchannel_id) or (reactionrole_ch_id)  from DB')

            else:
              message = self.getWelcomeMessage()
              message = message.replace('member.mention', member.mention).replace(
                  'botchannel_id', botchannel_id).replace('reactionrole_ch_id', reactionrole_ch_id)

              '''
              Check member for old role.  If exists, remove old role and add new role,
              then send welcome message to member join channel
              '''
              if old_role in member.roles:
                  await member.remove_roles(old_role)
                  await member.add_roles(new_role)
                  await member_ch.send(message)

    @welcome_command.error
    async def welcome_command_error(self, error, ctx):
        '''
        Error check, if command user or bot is missing permission, error message
        sent to command channel.
        Command and error message are auto-deleted after 30 seconds to keep
        channels clear of unnecessary error messages.
        '''
    
        if isinstance(error, MissingPermissions):
            await ctx.send('Sorry. You do not have permission to use that command.', delete_after=30)
            await ctx.message.delete(delay=30)
        elif isinstance(error, BotMissingPermissions):
            await ctx.send('The bot is missing \'Manage Roles\' permission.', delete_after=30)
            await ctx.message.delete(delay=30)

def setup(bot):
    bot.add_cog(OtherCommands(bot))

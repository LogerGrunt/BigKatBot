import os
import nextcord
from replit import db
from nextcord.ext import commands


class AnnouncePin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # replit will return an error if a DB item doesn't already exist
    def getDB(self, key):
        if key not in db.keys():
            return None
        else:
            return db[key]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Get information from reaction payload
        guild = self.bot.get_guild(payload.guild_id)
        owner = guild.get_member(int(os.environ.get('ADMINID', 0)))  # put your Discord ID here
        r_channel = self.bot.get_channel(payload.channel_id)
        r_message = await r_channel.fetch_message(payload.message_id)
        member = nextcord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        if payload.emoji.name == "📌":
            if r_channel.permissions_for(member).manage_messages:
                await r_message.pin()
        elif payload.emoji.name == "📣":

            announce_ch_id = self.getDB("announce_channel")
            if announce_ch_id is None:
                await owner.send(
                    "(AnnouncePin) There was an error getting the Announce channel ID from DB"
                )
            for channel in guild.channels:
                if str(channel.id) == announce_ch_id:
                    if channel.permissions_for(member).send_messages:

                        embed = nextcord.Embed(
                            title="Special Announcement!",
                            description=f"\n{r_message.content}",
                        )
                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name == "📌":
            guild = self.bot.get_guild(payload.guild_id)
            r_channel = self.bot.get_channel(payload.channel_id)
            member = nextcord.utils.find(
                lambda m: m.id == payload.user_id, guild.members
            )
            if r_channel.permissions_for(member).manage_messages:
                # Get information from reaction payload
                r_message = await r_channel.fetch_message(payload.message_id)

                await r_message.unpin()


def setup(bot):
    bot.add_cog(AnnouncePin(bot))

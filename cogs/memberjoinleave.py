import os
import nextcord
from replit import db
from nextcord.ext import commands


class MemberJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # replit will return an error if a DB item doesn't already exist
    def getDB(self, key):
        if key not in db.keys():
            return None
        else:
            return db[key]

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Event that takes place when a member is kicked or otherwise leaves the
        server.
        The message channel is retrieved from the config.json and an embed
        is sent to the configured channel - see `set` command to update channel.
        """
        # Get channel ID from config.json
        if member.bot:
            pass
        else:
            owner = member.guild.get_member(int(os.environ.get('ADMINID', 0)))  # your ID
            channel_id = int(self.getDB("member_leave_channel"))
            if channel_id is None:
                await owner.send(
                    "(on_member_remove) There was an error retrieving the channel ID from DB"
                )
            else:
                # Get channel object from ID stored in config.json
                channel = self.bot.get_channel(channel_id)

                # Get member info - joined date and ccount created date
                joined_at = member.joined_at.strftime("%d %b %Y")
                created_at = member.created_at.strftime("%d %b %Y")

                # Create the embedded message
                embed = nextcord.Embed(
                    title=f"{member.display_name} left the server!", color=0xC60000
                )
                if member.avatar is not None:
                    embed.set_thumbnail(url=member.avatar.url)
                else:
                    embed.set_thumbnail(
                        url="https://www.iconspng.com/uploads/primary-unknown/primary-unknown.png"
                    )
                embed.add_field(
                    name="User", value=f"{member.mention}\n{member}", inline=False
                )
                embed.add_field(name="Account Creation", value=created_at, inline=False)
                embed.add_field(name=f"Join Date", value=joined_at, inline=False)
                embed.set_footer(text=f"ID: {member.id}")

                # Send embed to channel
                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberJoinLeave(bot))

import dbwrapper
import logging
import nextcord

log = logging.getLogger('root')

class EventUtils(object):
    def __init__(self, bot):
        self.bot: nextcord.Client = bot

    def setBot(self, bot):
        self.bot: nextcord.Client = bot

    async def update_events_db(self):
        #we always want to get the latest info from the bot to store in the events DB
        #so it's just best to clear the DB and then reinsert with the updated into on bot startup

        with dbwrapper.DiscordDB() as dbobj:
            dbobj.Events_Clear()

            for guild in self.bot.guilds:
                async for event in guild.fetch_scheduled_events():
                    result = dbobj.Events_Get(guild.id, event.id)
                    if result is None:
                        eventObj = dbobj.Events_Add(guild.id, event.id, event.name, event.start_time, event.end_time)
                        if eventObj is None:
                            log.warning(f"[%s] There was an error adding event [{event.id}]!", "EventUtils")
                        else:
                            log.warning(f"[%s] DB Event Add [{event.id}] [{event.name}]", "EventUtils")


    async def get_userlist(self, guild_id, event_id):
        guildObj: nextcord.Guild = self.bot.get_guild(guild_id)
        eventObj: nextcord.ScheduledEvent = await guildObj.fetch_scheduled_event(event_id, with_users=True)

        if eventObj is not None:

            #grab the user list and update it
            async for usersObj in eventObj.fetch_users():
                print(usersObj.user_id, usersObj.user.name, usersObj.user.display_name)

        else:
            log.warning(f"[%s] Error Grabbing Userlist [{guild_id}] [{event_id}]", "EventUtils")


    def add_event(self, event:nextcord.ScheduledEvent):
        if event is not None:
            with dbwrapper.DiscordDB() as dbobj:
                eventObj = dbobj.Events_Add(event.guild.id, event.id, event.name, event.start_time, event.end_time)
                if eventObj is None:
                    log.warning(f"[%s] Event Add Error [{event.id}]!", "EventUtils")
        else:   
            log.warning(f"[%s] Error Adding Event [Null nextcord.ScheduledEvent]", "EventUtils")

    def remove_event(self, event:nextcord.ScheduledEvent):
        if event is not None:
            with dbwrapper.DiscordDB() as dbobj:
                dbobj.Events_Remove(event.guild.id, event.id)
        else:   
            log.warning(f"[%s] Error Removing Event [Null nextcord.ScheduledEvent]", "EventUtils")

    def update_event(self, after_event:nextcord.ScheduledEvent):
        if after_event is not None:
            with dbwrapper.DiscordDB() as dbobj:

                changed = dbobj.Events_Update(after_event.guild.id, after_event.id, after_event.name, after_event.start_time, after_event.end_time)

                if changed is False:
                    log.warning(f"[%s] Error -> Could not update event [{after_event.id}] [{after_event.name}]!", "EventUtils")
                else:
                    log.warning(f"[%s] Event Updated [{after_event.id}] [{after_event.name}] {after_event.start_time} | {after_event.end_time}!", "EventUtils")                    
        else:   
            log.warning(f"[%s] Error Updating Event [Null nextcord.ScheduledEvent]", "EventUtils")

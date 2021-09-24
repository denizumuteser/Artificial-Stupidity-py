import discord, time, random, platform, asyncio
from discord.ext import commands, tasks
import config

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.printer.start()


    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=60.0)
    async def printer(self):

        channel = self.client.get_channel({insert channel id here})  # channel 1
        
        result = time.localtime(time.time() + 0 * 3600)
        hour = result.tm_hour
        min = result.tm_min
        sec = result.tm_sec
        config.Current_Time = str(hour) + ":" + str(min)

        if hour == 10 and min == 0:
            await channel.send(random.choice(config.response_dict['morning_message']))
        elif hour == 0 and min == 0:
            await channel.send(random.choice(config.response_dict['night_message']))
        if min == 0:
            print(config.Current_Time, "|", "Running perfectly.")

def setup(client):
    client.add_cog(MyCog(client))
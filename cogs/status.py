import discord
from discord.ext import commands, tasks
from itertools import cycle

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.status = cycle(['Cogito', 'ergo', 'sum'])

    @tasks.loop(seconds=2.5)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))

    @commands.Cog.listener() # cog listener is same as 'event'
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.change_status.start()

def setup(client):
    client.add_cog(MyCog(client))
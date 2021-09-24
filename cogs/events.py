import discord
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f'Error. Try d.help ({error})')

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
            print(str(ctx.author).split("#")[0], "deleted:",  ctx.content)

def setup(client):
    client.add_cog(MyCog(client))
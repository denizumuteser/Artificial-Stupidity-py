import asyncio
import discord, random
from discord.ext import commands
import config


class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_message(self, ctx):
        
        if (ctx.author.bot):  # no self response
            return

        elif ctx.content.startswith("d."):
            return

        elif ctx.channel.id not in config.allowedChannels:
            return

        # sender of the message
        user = ctx.author.id

        random_for_responses = random.randint(1, 2)
        random_for_reactions = random.randint(1, 10)
        random_for_constant_responses = random.randint(1, 10)

        # curse responses
        for word in config.response_dict['curse']:
            if word in ctx.content.lower():
                await ctx.channel.send(random.choice(config.response_dict['curse_response']))
                return

        # question responses
        for word in config.response_dict['question']:
            if word in ctx.content.lower():
                await ctx.channel.send(random.choice(config.response_dict['question_response']))
                return
	# personal responses
	##deleted##	        

        # constant responses
        ##deleted##

        # random responses
        elif random_for_responses == 1:
            await ctx.channel.send(random.choice(config.response_dict['random_response']))
        #await self.client.process_commands(ctx)
     
def setup(client):
    client.add_cog(MyCog(client))

import discord, asyncio, time, os, random, platform
from discord.ext import tasks, commands
import config

intents = discord.Intents.all()

# Token for discord bot
TOKEN = open("token.txt", "r").readline()

# preix for calling bot commands
client = commands.Bot(command_prefix='d.', intents=intents)


# remove default help command
client.remove_command("help")

# connect all cogs
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded")
            raise e
        else:
            print("{} has been succesfully Loaded.".format(cog))

print("Bot is ready!")
print(platform.system())
client.run(TOKEN)
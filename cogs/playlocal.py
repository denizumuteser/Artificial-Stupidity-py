import discord, asyncio, random, os, platform
from discord.ext import commands
import config

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)  # play from local drive
    async def playlocal(self, ctx, name="random", id=0):
        global vc
        global playlist

        if len(self.client.voice_clients) != 0:
            vc = self.client.voice_clients[0]

        else:
            vc = None

        if name == "random":
            name = random.choice(config.local_list)

        if id == 0:
            voice_channel = ctx.author.voice
        else:
            voice_channel = self.client.get_channel(int(id))

        exist = os.path.exists("./sounds/%s.mp3" % name)
        if exist:
            if name not in config.playlist:
                config.playlist.append(name)
        else:
            await ctx.channel.send("No such audio file in the directory.")

        if voice_channel is not None and len(config.playlist) != 0:
            if vc is None or vc.channel != voice_channel.channel:
                if id == 0:
                    vc = await voice_channel.channel.connect()
                else:
                    vc = await voice_channel.connect()

            vc = self.client.voice_clients[0]
            if vc.is_playing():
                return
            while len(config.playlist) != 0:
                if vc is None:
                    vc = None
                    return
                current_playing = config.playlist.pop(0)

                if platform.system() == "Windows":
                    player_path = "./ffmpeg/bin/ffmpeg.exe"
                else:
                    player_path = "/usr/bin/ffmpeg"

                vc.play(discord.FFmpegPCMAudio(executable=player_path, source="./sounds/%s.mp3" % current_playing))
                while vc.is_playing():
                    await asyncio.sleep(0.5)
                    if vc is None:
                        break
            if vc is not None:
                await vc.disconnect()
            vc = None
        else:
            if ctx.author.voice == None:
                await ctx.send(str(ctx.author.name) + " is not in a voice channel.")
            vc = None

    @commands.command(pass_context=True)  # skip playing music
    async def skip(self, ctx):
        global vc
        if vc is None or not vc.is_playing():
            await ctx.channel.send("Nothing is playing...")
            vc = None
        else:
            await vc.disconnect()
            vc = None
        config.playlist = []

def setup(client):
    client.add_cog(MyCog(client))
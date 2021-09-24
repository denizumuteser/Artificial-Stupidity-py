import discord, asyncio, random, platform
from discord.ext import commands
import config

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fix(self, ctx):
        config.vc = None
        config.playlist = []
        config.bot_current_channel = None
        await ctx.channel.send("Health restored.")

    @commands.command()
    async def voiceinfo(self, ctx, user="self"):
        if user == "self":
            user = ctx.message.author.name
        for line in config.voices:
            if line[0] == user:
                await ctx.channel.send(line[2])

    @commands.command()
    async def setvoice(self, ctx, filename="", user="self", condition="in"):
        #await ctx.channel.send(ctx.message.author.name)
        old_file = open("voice_dict.txt","r")
        lines_listt = old_file.readlines()
        temp = []
        number = 0
        done = False
        
        #check filenames
        #test = filename.split(",")
        #for eachname in test:
        #    if not eachname in config.local_list:
        #        await ctx.channel.send("No audio with this name")
        #        return

        if user == "self":
            user = ctx.message.author.name

        # add voice to author or existing user
        for linee in lines_listt:
            temp = linee.split("||")
            if (temp[0] == user) and temp[1]==condition:
                temp[2] = filename
                new_line = str(temp[0]) + "||" + str(temp[1]) + "||" + str(temp[2]) + "\n"
                lines_listt[number] = new_line
                done = True
            number+=1
        
        if not done: #adding new user
                new_user = user + "||" + condition + "||" + filename
                lines_listt[len(lines_listt)-1] = lines_listt[len(lines_listt)-1] + "\n"
                lines_listt.append(new_user)

        old_file = open("voice_dict.txt","w")
        old_file.writelines(lines_listt)
        old_file.close()
        await ctx.channel.send("Voice set as {}".format(filename))

        config.voices = []
        with open('voice_dict.txt') as f:
            for line in f:
                line = line.split("\n")[0]
                split_line = line.split("||")
                split_line[2] = split_line[2].split(",")  # tracks
                config.voices.append(split_line)
        return     

    @commands.Cog.listener()  # play voice on voice channel connect
    async def on_voice_state_update(self, member, before, after):  # detects first time
        if member.id != 282632758688350209 and before.channel != after.channel and config.LOGGING: # print info about voice update
            print(config.Current_Time, "|", str(member).split("#")[0],": " ,before.channel, "->", after.channel)
        exist = False
        channel = None
        member_tracks = []
        if after.channel is None and before.channel is not None: # leaving voice channel
            for line in config.voices:
                if (line[0] == member.name) and (line[1] == "out"):
                    exist = True
                    member_tracks = line[2]
                    channel = before.channel
                    break

        elif before.channel is None and after.channel is not None:  # entering a voice channel
            for line in config.voices:
                if (line[0] == member.name) and (line[1] == "in"):
                    exist = True
                    member_tracks = line[2]
                    channel = member.voice.channel
                    break
        else:
            return
        if not exist: # not a member of voice dictionary
            return
        name = random.choice(member_tracks)
        if not name: # no assigned track name
            return
        if not name in config.local_list:
            return

        if name not in config.playlist:
            config.playlist.append(name)

        if channel is not None and len(config.playlist) != 0:
            if config.vc is None:
                if id == 0:
                    vc = await channel.channel.connect()
                else:
                    #if config.vc is not None:
                    vc = await channel.connect()

            elif config.vc.channel != channel.channel:
                if id == 0:
                    vc = await channel.channel.connect()
                    #print(vc.channel)
                else:
                    vc = await channel.connect()

            config.vc = self.client.voice_clients[0]
            if vc.is_playing():
                return

        if config.vc.channel != channel:
            vc = await channel.connect()

        while len(config.playlist) != 0:

            if platform.system() == "Windows":
                    player_path = "./ffmpeg/bin/ffmpeg.exe"
            else:
                player_path = "/usr/bin/ffmpeg"

            vc.play(discord.FFmpegPCMAudio(executable=player_path,
                                       source="./sounds/%s.mp3" % config.playlist.pop(0)))
            while vc.is_playing():
                await asyncio.sleep(0.5)
            await asyncio.sleep(0.2)
        await vc.disconnect()
        config.vc = None


def setup(client):
    client.add_cog(MyCog(client))
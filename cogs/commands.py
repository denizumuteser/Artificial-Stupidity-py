import discord, os, youtube_dl, datetime, platform
from discord.ext import commands
import config
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

async def downloadVideo(videourl):
    if platform.system() == "Windows":
        ydl = youtube_dl.YoutubeDL({
            'outtmpl': './y-dl/%(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4'})
    else:
        ydl = youtube_dl.YoutubeDL({
            'outtmpl': 'y-dl/%(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4'})
    ydl.download([videourl])

async def downloadMusic(videourl):

    if platform.system() == "Windows":
        ydl = youtube_dl.YoutubeDL({
        'outtmpl': './y-dl/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'ffmpeg_location': './ffmpeg/bin/ffmpeg.exe',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]})
    else:
        ydl = youtube_dl.YoutubeDL({
        'outtmpl': 'y-dl/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'ffmpeg_location': '/usr/bin/ffmpeg', #linux ffmpeg location
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]})
    ydl.download([videourl])

async def getinfo(videourl):
    ydl = youtube_dl.YoutubeDL()
    r = ydl.extract_info((videourl), download=False)
    return r


class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # make bot send your message
    @commands.command()
    async def whisper(self, ctx, id, *msg):
        msglist, text = list(msg), ""
        for word in msglist:
            text += word + " "
        channelid = self.client.get_channel(int(id))
        await channelid.send(text)

    # delete x number of recent messages
    @commands.command()
    async def clear(self, ctx, amount=5):
        if amount == "all":
            await ctx.channel.purge()
            return
        await ctx.channel.purge(limit=int(amount)+1)
    
    # bot reads your message as tts
    @commands.command()
    async def speak(self, ctx, *msg):
        msglist, text = list(msg), ""
        for word in msglist:
            text += word+" "
        await ctx.channel.send(text, tts=True)

    @commands.command()
    async def download(self, ctx):
        if ctx.message.attachments:
            split_v1 = str(ctx.message.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            print(filename)
            if filename in os.listdir('./sounds'):
                await ctx.channel.send("file with that name already exist in directory.")
                return
            if filename.endswith(".mp3"):
                await ctx.message.attachments[0].save(fp="./sounds/{}".format(filename))
                await ctx.channel.send("filed named {} saved successfully.".format(filename))

                config.local_list = os.listdir('./sounds')  # directory of local sounds
                config.local_list.sort()
                config.local_list_text = ""  # names of all sound files
                for i in range(len(config.local_list)):
                    ii = config.local_list[i].split(".")
                    config.local_list[i] = ii[0]
                    config.local_list_text += ii[0] + " "

            else:
                await ctx.channel.send("wrong file format, please give mp3")
        else:
            await ctx.channel.send("no attachments")    
    

    #test for spotify
    @commands.command()
    async def status(self, ctx):
        activity = ctx.author.activities[0]
        if activity.name == "Spotify":
            await ctx.channel.send(f"{ctx.author.name} is currently listening to {activity.title} by {activity.artist}")
        else:
            await ctx.channel.send("User is not listening to Spotify.")

    
    @commands.command()
    async def ydl(self, ctx, url, choice="m", start="", end=""):
        title = (await getinfo(url))['title']
        formats = (await getinfo(url))['formats']
        filesize = formats[-1]['filesize']
        duration_s = (await getinfo(url))['duration']
        duration = "0"+str(datetime.timedelta(seconds=duration_s))

        if choice == "v":
            choice_name = "video(mp4)"
        elif choice == "m":
            choice_name = "audio(mp3)"

        await ctx.channel.send(f"Requesting to download {title} as {choice_name}.")
        if filesize is not None:
            await ctx.channel.send(f"File size is {round(filesize/(1024.0 * 1024.0),2)} MB.")

            if filesize >= 104857600: #50 MB limit
                await ctx.channel.send("File is too big.")
                return

            if filesize >= 8388608 and choice == "v" and start == "" and end == "": #8 MB limit
                await ctx.channel.send("Discord upload limit is 8MB, file is too big to upload.")
                return
        else:
            await ctx.channel.send("Unknown file size.")

        await ctx.channel.send("Starting to download...")
        if choice == "m":
            await downloadMusic(url)
            if platform.system() == "Windows":
                path = f"./y-dl/{title}.mp3"
                targetpath = f"./y-dl/{title}-cut.mp3"
            else:
                path = f"y-dl/{title}.mp3"
                targetpath = f"y-dl/{title}-cut.mp3"
        elif choice == "v":
            await downloadVideo(url)
            if platform.system() == "Windows":
                path = f"./y-dl/{title}.mp4"
                targetpath = f"./y-dl/{title}-cut.mp4"
            else:
                path = f"y-dl/{title}.mp4"
                targetpath = f"y-dl/{title}-cut.mp4"
        # cut if asked
        if start != "" or end != "":
            if start == "":
                start = "00:00:00"
            if end == "":
                end = duration
            
            temp = datetime.datetime.strptime(start, "%H:%M:%S")
            startsec = (temp - datetime.datetime(1900, 1, 1)).total_seconds()
            temp = datetime.datetime.strptime(end, "%H:%M:%S")
            endsec = (temp - datetime.datetime(1900, 1, 1)).total_seconds()
            ffmpeg_extract_subclip(path, startsec, endsec, targetname=targetpath)
            os.remove(path)
            os.rename(targetpath, path)
            await ctx.channel.send("Sub clip extracted.")

        size = os.path.getsize(path)
        await ctx.channel.send(f"Current size is {round(size/(1024.0 * 1024.0),2)} MB.")
        await ctx.channel.send("Starting to uploading...")
        await ctx.channel.send(file=discord.File(path))
        #remove file after upload
        os.remove(path)
        
            
def setup(client):
    client.add_cog(MyCog(client))
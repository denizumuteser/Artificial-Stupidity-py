import discord
from discord.ext import commands
import config

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='Help : list of commands available')
        embed.add_field(name='d.playlocal', value='Plays an audio from local directory, add server id as a parameter to play in different channel')
        embed.add_field(name='d.skip', value='stop playing current audio')
        embed.add_field(name='d.convert', value='send and image with message "convert" to convert it into text.')
        embed.add_field(name='d.describe', value='send and image with message "describe" to receive description of the image.')
        embed.add_field(name='d.speak message', value='bot reads the given text to everyone in the text channel.')
        embed.add_field(name='d.whisper channel_id message', value='bot sends the given message to given channel.')
        embed.add_field(name='d.tts fileName language message', value='creates new audio from given text.')
        embed.add_field(name='d.clear numberofmessages', value='clear recent messages')
        embed.add_field(name='d.voiceinfo user', value='Display current intro and outro audios.')
        embed.add_field(name='d.setvoice audioName user in/out', value='Set intro/outro audio to given named local mp3 file.')
        embed.add_field(name='d.download [embeded mp3 file]', value='bot downloads given audio.')
        embed.add_field(name='d.locals', value="displays all sounds in the directory.")
        embed.add_field(name='d.ydl url [type="m" or "v"] [start_time] [end_time]', value="downloads music or video in the given url.")
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def locals(self, ctx):
        await ctx.channel.send("Local Sound files:")
        await ctx.channel.send(config.local_list_text)


def setup(client):
    client.add_cog(MyCog(client))
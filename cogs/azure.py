import discord, time
from discord.ext import commands
import config
# for azure recognition
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# azure
subscription_key = "insert here"
endpoint = "insert here"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # image to text conversion
    @commands.command()
    async def convert(self, ctx):
        
        file = ctx.message.attachments[0]
        print(file.filename + " is converted to text.")
        image_url = file.url
        recognize_handw_results = computervision_client.read(image_url, raw=True)

        operation_location_remote = recognize_handw_results.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]

        while True:
            get_handw_text_results = computervision_client.get_read_result(operation_id)
            if get_handw_text_results.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        output = ""
        if get_handw_text_results.status == OperationStatusCodes.succeeded:
            for text_result in get_handw_text_results.analyze_result.read_results:
                for line in text_result.lines:
                    output += line.text + "\n"

        await ctx.channel.send(output)


    # image recognition
    @commands.command()
    async def describe(self, ctx):

        file = ctx.message.attachments[0]
        print("Description of: " + file.filename)
        image_url = file.url
        image_1_features = ["description"]

        results = computervision_client.analyze_image(image_url, image_1_features)
        output = ""
        if len(results.description.captions) == 0:
            await ctx.channel.send("No description detected.")
        else:
            for caption in results.description.captions:
                output += caption.text + ", with confidence: " + str(round(caption.confidence * 100, 2)) + "%\n"

            await ctx.channel.send(output)


def setup(client):
    client.add_cog(MyCog(client))
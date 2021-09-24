import os
allowedChannels = [{insert allowed channel ids that bot can talk}]

LOGGING = True
Current_Time = ""
vc = None
playlist = []
bot_current_channel = None

# dictionary for locals
local_list = os.listdir('./sounds') # directory of local sounds
local_list.sort()
local_list_text = "" # names of all sound files
for i in range(len(local_list)):
    ii = local_list[i].split(".")
    local_list[i] = ii[0]
    local_list_text += ii[0] + " "

# dictionary for responses and inputs
response_dict = {}
with open('responses.txt') as f:
    for line in f:
        line = line.split("\n")[0]
        line_list = line.split("=")
        responses = line_list[1].split(" | ")
        d = {line_list[0] : responses}
        response_dict.update(d)

voices = []
with open('voice_dict.txt') as f:
    for line in f:
        line = line.split("\n")[0]
        split_line = line.split("||")
        split_line[2] = split_line[2].split(",")
        voices.append(split_line)

message_dict = []
with open('whatsapp_list.txt') as f:
    for line in f:
        line = line.split("\n")[0]
        split_line = line.split("||")
        message_dict.append(split_line)
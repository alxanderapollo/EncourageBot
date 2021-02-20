import discord

#first event, this is the event that will happen as soon as its working and the bot is ready for use
client = discord.Client()
#1. register the event
@client.event
#when the bot is ready this call will happen
async def on_ready():
  #print check when we have succesffuly logged in
  #zero is replaced with the clients user name
  print('we have logged in as {0.user}'.format(client)) 

#2.Next event is if the bot recives a message

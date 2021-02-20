import discord
import os

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
@client.event
async def on_message(message):
  #if the message is the author itself, do nothing
  if message.author == client.user:
    return 
  
  #if message is from a client return hello
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
#run the bot
#tokens are private
#getenv will get the token stored in the env file
client.run(os.getenv('TOKEN'))
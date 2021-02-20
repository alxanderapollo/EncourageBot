#discord library
import discord
#events
import os
#HTTP requests 
import requests
#HTTP requests ae returned as JSON so we need the lib
import json

#helper function - will return a quote from the API 
def get_Quote():
  response = requests.get("https://zenquotes.io/api/random") #return a random quote
  json_data = json.loads(response.text)#converting the response back into json 
  #now we have to get the data out of the JSON
  #q stands for quote
# string concatination dash is right before the persons name 
#a stands for author
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


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
  #example of how to use the bot
  #if message is from a client return hello
  # if message.content.startswith('$hello'):
  #   await message.channel.send('Hello!')
  if message.content.startswith('$inspire'):
    quote = get_Quote()
    await message.channel.send(quote)

#run the bot
#tokens are private
#getenv will get the token stored in the env file
client.run(os.getenv('TOKEN'))
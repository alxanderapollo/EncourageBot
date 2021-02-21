#discord library
import discord
#events
import os
#HTTP requests 
import requests
#HTTP requests ae returned as JSON so we need the lib
import json
import random
#calls the replit data base
from replit import db

#sad words is list  of words that a user can use
sad_words = ["sad","depressed","unhappy", "angry","miserable","depressing"]

#words to encourage a user who is sad
starter_encouragments=["cheer up!","hang in there"," you are a great person / bot!"]

#if not responding
if "responding" not in db.keys():
  db["responding"] = True 

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

#allow the user to update the encouragement listing
def update_encouragements(encouragingMessage):
  #db.keys() returns the list of keys already in the data base
  #append the new encouragement to the list
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouragingMessage) #append the new message to the list
    #save it to the database
    db["encouragements"] = encouragements
  else:
    #if there arent any encouragements in the data base then will create them
    db["encouragements"] = [encouragingMessage]

#give users the ability to delte encouragements
def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


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
  msg = message.content 
  #example of how to use the bot
  #if message is from a client return hello
  # if message.content.startswith('$hello'):
  #   await message.channel.send('Hello!')
  if message.content.startswith('$inspire'):
    quote = get_Quote()
    await message.channel.send(quote)

#if this is true it will respond to the sad words
  if db["responding"]:
  #modding so the encouragements now come from the database
  #options will be where the db looks to get encouragements
    options = starter_encouragments
    if "encouragements" in db.keys():
      options = options + db["encouragements"]


  #check for sad words from the users
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

 #allows the user to add a message -----------------------
  #new user submitted messages
  #if. a message from the user starts with new
  #then add the message to the db
  if msg.startswith("$new"):
    #array of a message that splits at new and returns the second element in the list 
    encouraging_message = msg.split("new ", 1)[1]
    update_encouragements(encouraging_message) #update the list of messages with the new encouraging message
    #send something back to the user to know its working properly
    await message.channel.send("New encouraging message added. ")

#allow a user to delete a message --------------------------------
  if msg.startswith("$del"):
    # if there are no encouragements in the data base already it will return a an empty list
    encouragements = [] #empty list
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1]) #we get the index of message we are going to delete
      delete_encouragements(index) #we delete the message
      encouragements= db["encouragements"]
    
    await message.channel.send(encouragements) 
  
  #will allows the user to see the totality of the list os messages
  #ability to list encouraging messages
  if msg.startswith("$list"):
    encouragements = [] #first check if the list is empty
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)


  #feature to allow the bot whether to respond to sad messages or not
  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on ")
    else:
      db["responding"] = False
      await message.channel.send("responding is off ")    

#run the bot
#tokens are private
#getenv will get the token stored in the env file
client.run(os.getenv('TOKEN'))
import discord
import requests
import math
import random
import time
from keep_online import keep_alive
import asyncio
import json
import openai
import os
from dotenv import load_dotenv
import numpy

load_dotenv()
bot_token = os.getenv('BOT-TOKEN')
openai.organization = os.getenv('ORG')
openai.api_key = os.getenv('API-KEY')
openai.Model.list()
#openai.Completion.create(model="text-davinci-003", prompt="Where is India?", temperature=0, max_tokens=7)


intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False
intents.message_content = True

intents.presences = True
intents.members = True
client = discord.Client(intents=intents)
channels_allowed = [1072846609462861834, 1073826272939102288, 1073826295164710953, 1074226380058923138]

memes_images_list = [
    "https://i.ytimg.com/vi/3O-RwnBmBvk/hqdefault.jpg",
    "https://pbs.twimg.com/media/EA36gs1X4AA72Zp.jpg:large",
    "https://i.ytimg.com/vi/-p-afebkXvU/maxresdefault.jpg",
    "https://media.tenor.com/f0eN4x6t3gAAAAAC/discord-memes.gif"
]
bot_commands = ["hi", "hru", "rolldice", "talktome", "tod", "question", "image"]
positive_inputs = ["yes", "Yes", "y", "Y", "yessir", "Yessir"]
negative_inputs = ["no", "No", "n", "N", "nosir", "Nosir"]

# Truth or Dare game
async def tod(message):
    truths = [
        "What are you most afraid of?", "What was your childhood nickname?", "What is your special talent?", "Can you speak a different language?", "What is something you have stolen?", "What is your dream job?", "Say 5 bad habits you have?", "What would you do with a million dollars if you ever won the lottery?", "What is the silliest thing you have an emotional attachment to?", "At what time do you wake up in the morning?", "Have you ever let someone take the blame for something you did?", "What lie have you told that hurt someone?", "What you do when you are alone at home?", "How many times a day do you eat?", "Which kind of food do you like the most?", "Favorite Place you like to visit?", "What is the most embarrassing thing your parents have caught you doing?", "What do you like about me?", "Say 5 negatives about me!", "Whom do you hate the most?", "Who do you love the most?"
        ]
    dares = [
        "Pick someone in this room and (lovingly) roast them for one minute straight.", "Let another person post an Instagram caption on your behalf.", "Hand over your phone to another player who can send a single text saying anything they want to anyone they want.", "Let the other players go through your phone for one minute.", "Smell another player's armpit.", "Smell another player's bare foot.", "Eat a bite of a banana peel.", "Do an impression of another player until someone can figure out who it is.", "Say pickles at the end of every sentence you say until it's your turn again.", "Imitate a TikTok star until another player guesses who you're portraying.", "Act like a chicken until your next turn.", "Talk in a British accent until your next turn.", "Send a heart-eye emoji to your crush's Instagram story.", "Call a friend, pretend it's their birthday, and sing them Happy Birthday to You.", "Name a famous person that looks like each player in the room.", "Show us your best dance moves.", "Eat a packet of hot sauce straight.", "Let another person draw a tattoo on your back with a permanent marker.", "Put on a blindfold and touch the other players' faces until you can figure out who's who.", "Bite into a raw onion without slicing it.", "Go outside and try to “summon” the rain as loud as possible.", "Serenade the person to your right for a full minute.", "Do 20 squats.", "Let the other players redo your hairstyle.", "Eat a condiment of your choice straight from the bottle.", "Dump out your purse, backpack, or pockets and do a show and tell of what's inside.", "Let the player to your right redo your makeup with their eyes closed.", "Prank call one of your family members.", "Let another player create a hat out of toilet paper — and you have to wear it for the rest of the game.", "Do a plank for a full minute.", "Do your sassiest runway walk.", "Put five ice cubes in your mouth (you can't chew them, you just have to let them melt—brrr).", "Bark like a dog until it's your next turn.", "Draw your favorite movie and have the other person guess it (Pictionary-style).", "Repeat everything the person to your right says until your next turn.", "Demonstrate how you style your hair in the mirror (without actually using the mirror).", "Play air guitar for one minute.", "Empty a glass of cold water onto your head outside.", "Go on Instagram Live and do a dramatic reading of one of your textbooks.", "In the next 10 minutes, find a way to scare another player and make it a surprise.", "Lick a bar of soap.", "Talk to a pillow as if it's your crush.", "Post the oldest selfie on your phone to Snapchat or Instagram stories (and leave it up!).", "Attempt the first TikTok dance on your FYP.", "Imitate a celebrity of the group's choosing every time you talk for the next 10 minutes.", "Go to your crush's Instagram page and like something from several weeks ago.", "Do karaoke to a song of the group's choosing.", "Post a photo (any photo) to social with a heartfelt dedication to a celebrity of the group's choosing.", "Find your very first crush on social and DM them.", "Peel a banana using just your toes."
        ]
    bot_replies = ["ok but who cares LOL", "damn.", "cool now kys", "wow now shut up", "Great!", "ok and"]
    await message.reply("*Mention another player to play with*")
    user_reply = await client.wait_for("message", 
    check=lambda SentMessage: SentMessage.author == message.author and SentMessage.channel == message.channel, 
    timeout=60)
    if len(user_reply.mentions) == 1 and user_reply.mentions[0].bot == False and user_reply.mentions[0].id != message.author.id:
        print(user_reply.mentions)
        second_user_ID = user_reply.mentions[0].id
        second_user_name = user_reply.mentions[0].name
        second_user = user_reply.mentions
        try:
            await message.channel.send(f"<@{second_user_ID}>, {message.author.name} wants to play T or D with you. [y/n]")
            challenge = await client.wait_for("message", 
                        check=lambda SentMessage: SentMessage.author.name == second_user_name and SentMessage.channel == message.channel, 
                        timeout=60)
            if challenge.content in positive_inputs:
                challenge_embed = discord.Embed(color=discord.Color.green(), title=f"**{second_user_name}** has accepted {message.author.name}'s request!")
                await message.channel.send(embed=challenge_embed)
                await asyncio.sleep(1)
                await message.channel.send("*Game starting...*")
                await asyncio.sleep(2)
                await message.channel.send("*Message first to start.*")
                try:
                    start_mssg = await client.wait_for("message", 
                            check=lambda SentMessage: SentMessage.channel == message.channel, 
                            timeout=60)
                    if start_mssg.author.id == user_reply.author.id:
                        first_player = start_mssg.author
                        first_player_name = first_player.name
                        second_player = second_user
                        second_player_name = second_user_name
                    elif start_mssg.author.id == second_user_ID:
                        first_player = second_user
                        first_player_name = second_user_name
                        second_player = message.author
                        second_player_name = second_player.name
                    start_embed = discord.Embed(color=discord.Color.blue(), title=f"**{first_player_name}** will be starting.", description=f"{second_player_name} isn't so fast after all.")
                    print(f"First player - {first_player_name}")
                    print(f"Second player - {second_player_name}")
                    await message.channel.send(embed=start_embed)
                    last_message = [message async for message in message.channel.history(limit=1)]
                    while "exit" != last_message[0].content:
                        #First player chance                  
                        question_embed = discord.Embed(color=discord.Color.blue(), title=f"**{first_player_name}**, Truth or Dare")
                        question_embed.set_footer(text="your mom")
                        
                        await message.channel.send(embed=question_embed)
                        answer = await client.wait_for("message", 
                                check=lambda SentMessage: SentMessage.author.name == first_player_name and  SentMessage.channel == message.channel, 
                                timeout=60)
                        if answer.content == "truth" or answer.content == "Truth":
                            truth = random.choice(truths)
                            answer_embed = discord.Embed(color=discord.Color.gold(), title=f"**{truth}**")
                            await answer.reply(embed=answer_embed)
                        elif answer.content == "dare" or answer.content == "Dare":
                            dare = random.choice(dares)
                            answer_embed = discord.Embed(color=discord.Color.white(), title=f"**{dare}**")
                            await answer.reply(embed=answer_embed)
                        player_answer = await client.wait_for("message", 
                                check=lambda SentMessage: SentMessage.author.name == first_player_name and  SentMessage.channel == message.channel, 
                                timeout=60)                        
                        chances = random.randint(1,10)
                        if chances == 7:
                            answer_reply = discord.Embed(color=discord.Color.brand_red(), title=f"**{random.choice(bot_replies)}**")
                            await player_answer.channel.send(embed=answer_reply)
                            
                        #Second player chances
                        question_embed = discord.Embed(color=discord.Color.blue(), title=f"**{second_player_name}**, Truth or Dare")
                        question_embed.set_footer(text="your mom")
                        
                        await message.channel.send(embed=question_embed)
                        answer = await client.wait_for("message", 
                                check=lambda SentMessage: SentMessage.author.name == second_player_name and  SentMessage.channel == message.channel, 
                                timeout=60)
                        if answer.content == "truth" or answer.content == "Truth":
                            truth = random.choice(truths)
                            answer_embed = discord.Embed(color=discord.Color.gold(), title=f"**{truth}**")
                            await answer.reply(embed=answer_embed)
                        elif answer.content == "dare" or answer.content == "Dare":
                            dare = random.choice(dares)
                            answer_embed = discord.Embed(color=discord.Color.white(), title=f"**{dare}**")
                            await answer.reply(embed=answer_embed)
                        else:
                            return
                        player_answer = await client.wait_for("message", 
                                check=lambda SentMessage: SentMessage.author.name == second_player_name and  SentMessage.channel == message.channel, 
                                timeout=60)
                        chances = random.randint(1,10)
                        if chances == 7:
                            answer_reply = discord.Embed(color=discord.Color.brand_red(), title=f"**{random.choice(bot_replies)}**")
                            await player_answer.channel.send(embed=answer_reply)
                    print("exit out of loop.")
                except asyncio.TimeoutError:
                    await start_mssg.reply("Time ran out!")
            elif challenge.content in negative_inputs:
                challenge_embed = discord.Embed(color=discord.Color.red(), title=f"**{second_user_name}** has denied {message.author.name}'s request!")
                await message.channel.send(embed=challenge_embed)
                return
            else:
                challenge_embed = discord.Embed(color=discord.Color.red(), title=f"**Not a valid response**")
                await message.channel.send(embed=challenge_embed)
                return
        except asyncio.TimeoutError:
            await message.channel.send("Did not reply in time.")
    elif not user_reply.mentions or user_reply.mentions[0].bot == True or user_reply.mentions[0].id == message.author.id:
        await user_reply.reply("*Not a valid member, Restarting...*")
        await asyncio.sleep(2)
        return await tod(message)
    elif len(user_reply.mentions) > 1:
        await user_reply.reply("*Mention only one user please, Restarting...*")
        await asyncio.sleep(2)
        return await tod(message)
    
    
#Member join 
@client.event
async def on_member_join(member):
    embed = discord.Embed(color=discord.Color.gold(),
                                 title=f"Welcome to the server **{member.name}**!")
    embed.set_author(name=client.user)
    await member.send(embed=embed)
#Member left
@client.event
async def on_member_left(member):
    embed = discord.Embed(color=discord.Color.red(),
                                 title=f"Imagine leaving, big L!")
    embed.set_author(name=client.user)
    await member.send(embed=embed)
#Member banned
@client.event
async def on_member_ban(member):
    embed = discord.Embed(color=discord.Color.red(),
                                 title=f"**Bro got banned LMAO**")
    embed.set_author(name=client.user)
    await member.send(embed=embed)
#Member kicked

@client.event
async def on_member_kick(member):
    embed = discord.Embed(color=discord.Color.red(),
                                 title=f"**Get kicked loser!**")
    embed.set_author(name=client.user)
    await member.send(embed=embed)
#Bot ready event
@client.event
async def on_ready():
    print("Bot is logged in as", client.user)


def rollDice():
    return f"Dice rolled a **{random.randint(1,6)}**"

#User send message event
@client.event
async def on_message(message):
    #List of bot responses
    bot_responses = {
        "hi": random.choice([f"Hey there **{message.author.name}**", f"Hello {message.author.name}, how's your day so far?", f"Wsg cuh, how's life?"]),
        "hru": random.choice(["I'm good, how are you?", "I'm alright, could be better.", "Eh, I need rest."]),
        "rolldice": rollDice()
    }
    
    prefix = '-'
    command_ongoing = False
    if message.author == client.user:
        return
    
    if message.channel.id == 1074227053068554250 and message.content[0:] == "image" or message.content[0:] == "Image":  
        print(message.content)
        print("Generating image")
        await message.reply("Please enter the name of the image.")
        user_message = await client.wait_for("message", 
                    check=lambda SentMessage: SentMessage.author == message.author and SentMessage.channel == message.channel, 
                    timeout=60)
        try:
            await message.channel.send("*Generating Image...*")
            print(f"Image requested by {message.author}")
            response = openai.Image.create(
            prompt=user_message.content,
            n=1,
            size="512x512"
        )
            image_url = response['data'][0]['url']
        
            embed = discord.Embed(color=discord.Color.dark_magenta(), title=f"Image generation for - {user_message.content}")
            embed.set_image(url=image_url)
            await message.reply(embed=embed)
            print(f"Image sent. url- {image_url}")
        except asyncio.TimeoutError:
            await message.reply("Time ran out!")

    if message.content[0] == prefix and message.channel.id in channels_allowed and command_ongoing == False and len(message.mentions) == 0:
        print("User Message -", str(message.content))
        for i in bot_responses:
            if message.content[1:] == i.lower() and command_ongoing == False:
                command_ongoing = True
                message_to_send = bot_responses[i]
                await message.reply(message_to_send)
                command_ongoing = False
                print("Message sent")
                return
            elif message.content[1:] == "help" and command_ongoing == False:
                command_ongoing = True
                print(len(message.content))
                await message.author.send(
                    f"**Here is a list of commands -** \n {str(bot_commands)}"
                )
                command_ongoing = False
                return 
            elif message.content[1:] == "talktome" and command_ongoing == False:
                command_ongoing = True
                await message.reply("Later.")
                command_ongoing = False
                return

            elif message.content[1:] == "question" and command_ongoing == False:
                command_ongoing = True
                print(command_ongoing)
                try:
                    print(len(message.content))
                    await message.channel.send("Please ask your question.")
                    user_response = await client.wait_for("message", 
                    check=lambda SentMessage: SentMessage.author == message.author and SentMessage.channel == message.channel, 
                    timeout=60)
                    generating_mssg = await message.channel.send("*Generating response...*")
                    answer = openai.Completion.create(
                        model="text-davinci-003", 
                        prompt=user_response.content, 
                        temperature=0.7, 
                        max_tokens=256
                        )

                    answer_text = answer.choices[0]["text"]
                    answer_embed = discord.Embed(color=discord.Color.green(), title="*Your Answer*", description=answer_text)
                    answer_embed.set_author(name=client.user)
                    await user_response.reply(embed=answer_embed)
                    print(answer.choices)
                    command_ongoing = False
                except asyncio.TimeoutError:
                    await message.reply("Time ran out!")
                    command_ongoing = False
                return
            elif message.content[1:] == "tod":
                await tod(message)
                return
                
                
        await message.reply(
            f"*I'm sorry but I'm unable to understand that command.*")

#User edit message
@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return

    embed = discord.Embed(color=discord.Color.red(),
                          title="Hah! You really thought?",
                          description=f"**Old message:** {before.content}\n**New message:** {after.content}"
                          )
    embed.set_footer(text="bro thought")
    embed.set_image(url="https://i.kym-cdn.com/entries/icons/original/000/037/073/bozocover.jpg")
    await before.reply(embed=embed)

keep_alive()
client.run(bot_token)

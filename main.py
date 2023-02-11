import discord
import os
import requests
import math
import random
import time
from keep_online import keep_alive
import asyncio
import json
import openai
from dotenv import load_dotenv

load_dotenv()
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
channels_allowed = [1072846609462861834, 1073826272939102288, 1073826295164710953]

memes_images_list = [
    "https://i.ytimg.com/vi/3O-RwnBmBvk/hqdefault.jpg",
    "https://pbs.twimg.com/media/EA36gs1X4AA72Zp.jpg:large",
    "https://i.ytimg.com/vi/-p-afebkXvU/maxresdefault.jpg",
    "https://media.tenor.com/f0eN4x6t3gAAAAAC/discord-memes.gif"
]

#Member join event
@client.event
async def on_member_join(member):
    welcomeEmbed = discord.Embed(color=discord.Color.red(),
                                 title=f"Welcome to the server **{member.name}**!")
    welcomeEmbed.set_author(name=client.user)
    await member.send(embed=welcomeEmbed)
#Member left
@client.event
async def on_member_left(member):
    welcomeEmbed = discord.Embed(color=discord.Color.red(),
                                 title=f"Imagine leaving, big L!")
    welcomeEmbed.set_author(name=client.user)
    await member.send(embed=welcomeEmbed)
#Member banned
@client.event
async def on_member_ban(member):
    welcomeEmbed = discord.Embed(color=discord.Color.red(),
                                 title=f"**Bro got banned LMAO**")
    welcomeEmbed.set_author(name=client.user)
    await member.send(embed=welcomeEmbed)

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
    if message.content[0] == prefix and message.channel.id in channels_allowed and command_ongoing == False:
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
                    f"**Here is a list of commands -** \n {list(bot_responses.keys())}"
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
                    timeout=10)
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
        await message.reply(
            f"I'm sorry but I'm unable to understand that command. \n You could try using one of these instead \n {list(bot_responses)} \n *Note- These are only the basic commands available. Other commands are not listed above*")

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
client.run(os.getenv('BOT-TOKEN'))

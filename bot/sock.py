import os
import asyncio
import discord
from dotenv import load_dotenv

from main import bot_main

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$wiki'):
        await message.channel.send('Send with format: $first article | secondarticle')

    elif message.content.startswith('$'):
        content = message.content[1:] # removes '$'
        content = content.split("|")
        article1 = content[0]
        article2 = content[1]

        articles = await (bot_main(article1, article2))
        print(articles)
        await message.channel.send(articles)




client.run(os.getenv('TOKEN'))

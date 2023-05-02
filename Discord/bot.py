#Discord Voice Assistent 
#Permissions = 36715520

import os
import random
import discord
from discord.ext import commands
from discord_token import DISCORD_TOKEN
import sys
sys.path.insert(1, './')
from FinalModel.bot import chat


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '', intents=intents)
# client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')



@client.event
async def on_member_join(member):
    channel = client.get_channel(member)
    await channel.send(f'Hello!, {member.name} welcome', tts=True)



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('hi') :
        await message.channel.send(f'Hello! {message.author.name}', tts=True)
    else :
        await message.channel.send(chat(message.content))



@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is not None and after.channel is None:
        msg = 'left'
        channel = before.channel
    elif before.channel is None and after.channel is not None:
        msg = 'joined'
        channel = after.channel
    await channel.send(f'{member.name} has {msg} the voice', tts=True)



@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if ctx.author.voice:
        voice_channel = await channel.connect()
        ctx.send("Joined Voice")
    else:
        ctx.send(f"{ctx.message.author.name} not in voice")



@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send('I am not in voice')


client.run(DISCORD_TOKEN)

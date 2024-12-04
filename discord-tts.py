import discord
from discord.ext import commands
import sys
import io
import logging
import asyncio
import requests
import time
import os
import urllib.request
# Enable Intents
intents = discord.Intents.all()  # Enable all intents
intents.messages = True  # Allow the bot to receive messages

# Create instance of Bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)  # Set the prefix

url = "https://api-voice.botnoi.ai/openapi/v1/generate_audio"
payload = {
    "text": "ทดสอบภาษาไทย 1234 test english hello my name is",
    "speaker": 63,
    "volume": 1,
    "speed": 1,
    "type_media": "mp3",
    "save_file": "true",
    "language": "th",
}
headers = {
'Botnoi-Token': 'bGFlZENCZE54SGFzYUgwaFRoRUxFTDYwQjNIMjU2MTg5NA==',
'Content-Type': 'application/json'
}
#response = requests.request("POST", url, headers=headers, json=payload)


async def create_v(message, channel):
    #data = {'input_text': message, 'speaker': 0, 'phrase_break': iPhrase_break, 'audiovisual': 0}
    print(channel)
    print(type(channel))
    aaa = message.split('%')
    speaker_s = 307
    message1 = message
    if len(aaa) > 1 :
        speaker_s = aaa[1]
        message1 = aaa[0]
    print(aaa)
    payload = {
    "text": message1,
    "speaker": speaker_s,
    "volume": 1,
    "speed": 1,
    "type_media": "mp3",
    "save_file": "true",
    "language": "th",
    }

    list
    response = requests.request("POST", url, headers=headers, json=payload)
    #response = requests.post(url, json=data, headers=headers)
    rr = response.json()
    if 'message' not in rr:

        if rr['point'] != 0:
            file_name = rr['audio_url']

            urllib.request.urlretrieve(file_name, f'test.mp3')

            voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
            if voice_client is None:
                voice_client = await channel.connect()

            if not voice_client.is_playing():
                voice_client.play(discord.FFmpegPCMAudio(f'test.mp3'), after=lambda e: print('done', e))
                print(f"Playing: {file_name}")

            if not voice_client.is_playing():
                voice_client.play(discord.FFmpegPCMAudio(f'test.mp3'), after=lambda e: print('done', e))
                print(f"Playing: {file_name}")
        else :
            print("cant speak na")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")
     
    if message.channel.name == 'tts' or message.channel.id == 988359881931239455 :
    #if message.content.startswith('สังเคราะห์เสียง'):
        if message.author.voice:
            channel = message.author.voice.channel
            cc = message.content
            aaa = cc.split('%') 
            list1 = [61, 63, 67, 70, 78, 79, 59, 60, 65, 69, 64, 66, 68, 71, 74, 62, 72, 73, 81, 82, 95, 100, 103, 107, 142, 145, 146, 80, 83, 96, 98, 141, 147, 84, 94, 99, 115, 119, 140, 148, 97, 102, 101, 104, 114, 139, 143, 144, 163, 154, 215, 225, 220, 224, 221, 222, 217, 214, 218, 223, 216]
            

            await create_v(message.content, channel)
            
            #if len(aaa) > 1 :
            #     if int(aaa[1]) not in list1 :
            #         await message.channel.send(f"ใช้แค่ในlist โว้ย \n {list1}")

            #     else: 
            #         await create_v(message.content, channel)
            # else:
            #     await create_v(message.content, channel)
        else:
            await message.channel.send("Please join a voice channel first.")

    await bot.process_commands(message)  # Process commands after custom message handling

@bot.command()
async def greet(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

@bot.command()
async def join(ctx):
    # ตรวจสอบว่าผู้ใช้ที่รันคำสั่งอยู่ใน Voice Channel หรือไม่
    if ctx.author.voice:
        channel = ctx.author.voice.channel

        # ตรวจสอบว่าบอทได้เชื่อมต่อกับ Voice Channel หรือยัง
        if ctx.voice_client is not None:
            if ctx.voice_client.channel == channel:
                await ctx.send("I am already connected to your voice channel!")
            else:
                await ctx.voice_client.move_to(channel)
                await ctx.send(f"Moved to {channel.name}")
        else:
            await channel.connect()
            await ctx.send(f"Joined {channel.name}")
    else:
        await ctx.send("You need to join a voice channel first.")


@bot.command()
async def play(ctx, url):
    voice_client = ctx.voice_client
    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegPCMAudio(url, executable="C:/ffmpeg/bin/ffmpeg.exe"), after=lambda e: print('done', e))
        await ctx.send(f"Now playing: {url}")
    else:
        await ctx.send("Already playing something.")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Stopped the music.")
    else:
        await ctx.send("No music is playing.")

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect()
    else:
        await ctx.send("I am not connected to a voice channel.")

bot.run('Key')  # Replace with your token

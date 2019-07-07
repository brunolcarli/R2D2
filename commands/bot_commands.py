import discord
from discord.ext import commands


client = commands.Bot(command_prefix='r2/')

@client.event
async def on_ready():
    print("BIP BIP READY!")

@client.command()
async def ping(bot):
    await bot.send('bip pong')

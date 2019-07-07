import discord
from discord.ext import commands
from decouple import config



client = commands.Bot(command_prefix='r2/')

@client.event
async def on_ready():
    print("BIP BIP READY!")

@client.command()
async def ping(bot):
    await bot.send('bip pong')

@client.command()
async def repo(bot, repo_name=''):
    '''
    Returns the link to civil cultural gitlab repository.
    '''
    repo_url = config('GITLAB_REPO') + '/{}'.format(repo_name)
    await bot.send(repo_url)

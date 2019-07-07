import discord
from discord.ext import commands
from decouple import config
import requests
import json
from random import choice
from commands.queries import get_quote_mutation
from settings import LISA_URL



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

@client.command()
async def quote(bot, *phrase):
    '''
    Saves a quoted message to be forever remembered.
    '''
    if phrase:
        message = ' '.join(word for word in phrase)
        payload = get_quote_mutation(message)

        headers = {
            'content-type': "application/json"
        }
        
        response = requests.request("POST", LISA_URL, data=payload, headers=headers)
        response = json.loads(response.text)
        response = response['data']['createR2Quote'].get('response')

    else:
        response = 'Insira alguma mensagem!'
        response += '\n`r2/quote foo baz`'

    await bot.send(response)

@client.command()
async def random_quote(bot):
    '''
    Returns a random quote
    '''
    payload = "{\"query\":\"query{\\n  r2Quotes\\n}\"}"
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", LISA_URL, data=payload, headers=headers)
    response = json.loads(response.text)
    quotes = response['data'].get('r2Quotes')

    await bot.send(choice(quotes))

@client.command()
async def remember(bot):
    '''
    Remembers you something important
    '''
    await bot.send('`LEIAM A DOCUMENTAÇÃO!`')

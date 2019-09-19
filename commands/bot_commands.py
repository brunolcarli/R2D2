# -*- coding: utf-8 -*-
"""
PT-Br: Módulo de comandos do Bot, aqui concentram-se os comandos principais
do bot.

English: Main command module. Here will be stacked all the commands the bot
has.
"""
import json
from random import choice
import discord
from discord.ext import commands
from decouple import config
import requests
from commands.queries import get_quote_mutation
from settings import LISA_URL


client = commands.Bot(command_prefix='r2/')


@client.event
async def on_member_join(member):
    print('Member joined')


@client.event
async def on_ready():
    print("BIP BIP READY!")


@client.command()
async def ping(bot):
    """
    Pings the bot to tests its execution.
    """
    await bot.send('bip pong...')


@client.command()
async def repo(bot, repo_name=''):
    """
    Returns the link to civil cultural gitlab repository.
    """
    repo_url = config('GITLAB_REPO') + '/{}'.format(repo_name)
    await bot.send(repo_url)


@client.command()
async def quote(bot, *phrase):
    """
    Saves a quoted message to be forever remembered.
    """
    if not phrase:
        await bot.send(
            'Insira alguma mensagem!\nEx:\n\n```r2/quote foo baz```'
        )
        return

    message = ' '.join(word for word in phrase)

    # A mensagem enviada é uma string hexadecimal
    payload = get_quote_mutation(message.encode('utf-8').hex())

    headers = {
        'content-type': "application/json"
    }

    response = requests.request(
        'POST',
        LISA_URL,  # TODO This API will soon be changed, get another backend
        data=payload,
        headers=headers
    )
    response = json.loads(response.text)

    try:
        response = response['data']['createR2Quote'].get('response')
        response = bytes.fromhex(response).decode('utf-8')
    except:
        response = 'Ops algo de errado aconteceu... Bip Bip'
        await bot.send(response)


@client.command()
async def random_quote(bot):
    """
    Returns a random quote.
    """
    payload = "{\"query\":\"query{\\n  r2Quotes\\n}\"}"
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", LISA_URL, data=payload, headers=headers)
    response = json.loads(response.text)
    try:
        quotes = response['data'].get('r2Quotes')
    except:
        bot_response = 'Ops algo deu errado Bip Bop...'
    else:
        chosen_quote = choice(quotes)
        bot_response = bytes.fromhex(chosen_quote).decode('utf-8')

    await bot.send(bot_response)


@client.command()
async def remember(bot):
    """
    Remembers you something important.
    """
    await bot.send('\n\n```LEIAM A DOCUMENTAÇÃO!```')

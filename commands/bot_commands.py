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
from settings import LISA_URL, GENERAL_CHANNEL, R2ID
from utils.nlp import (get_offense_level, get_the_right_answer,
                       binary_wordmatch, text_classifier,
                       basic_preprocess)

from utils.output_vectors import (opinions, insufficiency_recognition,
                                  offended)



client = commands.Bot(command_prefix='r2/')


@client.event
async def on_message(message):
    """
    Handler for chat event messages.
    """

    # Processa somente mensagens que não são do próprio R2D2
    if message.author.id == int(R2ID):
        return

    bot_mention = f'<@{R2ID}>'
    channel = message.channel

    # Não processa mensagens designadas à outros membros
    if '@' in message.content and bot_mention not in message.content:
        return

    greeting_msgs = [
        'oi', 'olá', 'saudações', 'namastê', 'bom dia', 'boa tarde'
    ]

    # Mensagens de despedida
    byebye_msgs = [
        'tchau', 'até logo', 'até mais', 'até breve', 'adeus', 'bye', 'ciao'
    ]
    try:
        chat_message = basic_preprocess(message.content)
    except Exception as ex:
        # TODO fazer um log melhor disso
        print(ex)
    else:
        # Se a mensagem enviada for um cumprimento
        if binary_wordmatch(chat_message, greeting_msgs):
            await channel.send(
                f'{choice(greeting_msgs).capitalize()} <@{message.author.id}>!'
            )

        # se for uma mensagem de despedida
        elif binary_wordmatch(chat_message, byebye_msgs):
            await channel.send(
                f'{choice(byebye_msgs).capitalize()} <@{message.author.id}>!'
            )

        try:
            is_offensive, offensivness = get_offense_level(
                basic_preprocess(message.content.lower())
            )
        except Exception as ex:
            # TODO escrever um log adequado
            print(ex)

        else:
            # se for ofensivo
            if is_offensive:
                await channel.send(choice(offended))


@client.event
async def on_member_join(member):
    """
    Sends a welcome message when a new user comes at the server.
    """
    # TODO melhorar essa mensagemd e boas vindas com um embedding bem bonito
    channel = client.get_channel(GENERAL_CHANNEL)
    await channel.send('\n\n```BEM VINDO```\n\n```WELCOME```\n\n')
    return


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

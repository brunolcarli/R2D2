import json
import requests
import discord
from discord.ext import commands




client = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix='r2/'
)

@client.event
async def on_ready():
    print("BIP BIP READY!")

@client.command()
async def ping(ctx):
    await ctx.send('bip pong')

@client.command()
async def request(ctx, method='get', url=None, response_key=None, *payload):
    """
    Send a HTTP Request to a endpoint
    """
    # if not params:
    #     return await ctx.send('Params not informed (METHOD, URL, PAYLOAD<optional>)')
    

    if not url:
        return await ctx.send('Need to specify a URL!')

    method = method.lower().strip()
    if method == 'get':
        r = requests.get(url)
        if r.status_code != 200:
            return await ctx.send(f'Failed requesting endpoint with http error {r.status_code}')
        if response_key is None:
            response = f'''
            ```json
                {json.dumps(r.json(), indent=3)}
            ```
            '''
        else:
            response = f'''
            ```json
                {json.dumps(r.json()[response_key], indent=3)}
            ```
            '''
        if len(response) > 3999:
            await ctx.send('Response is too large, try specify one of the keys:')
            return await ctx.send(list(r.json().keys()))
        return await ctx.send(response)
    
    if method == 'post':
        if not payload and response_key is None:
            return await ctx.send('Need to specify post payload')
        if response_key and not payload:
            response_key, payload = payload, response_key

        payload = ''.join(payload)
        payload = payload.replace("'", '"')
        payload = payload.replace('"', '\"')
        print(payload)
        try:
            payload = json.loads(payload)
        except Exception as err:
            print(err)
            return await ctx.send('Invalid json payload')

        r = requests.post(url, json=payload)
        if r.status_code != 200:
            return await ctx.send(f'Failed requesting endpoint with http error {r.status_code}')
        if response_key is None:
            response = f'''
            ```json
                {json.dumps(r.json(), indent=3)}
            ```
            '''
        else:
            response = f'''
            ```json
                {json.dumps(r.json()[response_key], indent=3)}
            ```
            '''
        if len(response) > 3999:
            await ctx.send('Response is too large, try specify one of the keys:')
            return await ctx.send(list(r.json().keys()))
        return await ctx.send(response)
    return await ctx.send('Invalid or not implemented method')

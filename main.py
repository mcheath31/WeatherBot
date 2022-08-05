import discord
import os
import requests
import json
from weather import error_message
from weather import parse_data
from weather import weather_message

command_prefix = "!weather "
my_secret = os.environ['api_key']
token = os.environ['TOKEN']

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name='!weather [location]'))


@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(
            command_prefix):
        if len(message.content.replace(command_prefix, ' ')) >= 1:
            location = message.content.replace(command_prefix, '').lower()
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={my_secret}&units=imperial'
            try:
                data = parse_data(
                    json.loads(requests.get(url).content)['main'])
                await message.channel.send(
                    embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))


client.run(token)

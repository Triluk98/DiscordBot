from asyncio import sleep
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)


@client.event
async def on_ready():
    fp = open("boticon.png", "rb")
    icon = fp.read()
    await sleep(10)
    await client.user.edit(avatar=icon)


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run('ODY2MTIxMjQwODg0NTQzNTAw.YPN8Qw.LzeILCBBYy02zBUFaXESvHwhjms')

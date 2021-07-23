from asyncio import sleep
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)


def change_icon():
    fp = open("boticon.png", "rb")
    icon = fp.read()
    client.user.edit(avatar=icon)


@client.event
async def on_ready():
    print("Bot online.")
    channel = client.get_channel(id=802602247983857717)
    # if not client.is_closed():
        # await channel.send("I'm back bitches. :^)")
    # change_icon()


@client.command()
async def load(ctx, extension):
    """Loading all Cogs"""
    client.load_extension(f'Cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    """Unloading all Cogs"""
    client.unload_extension(f'Cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    """Reloading (unload + load) all Cogs"""
    client.unload_extension(f'Cogs.{extension}')
    client.load_extension(f'Cogs.{extension}')


for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run('ODY2MTIxMjQwODg0NTQzNTAw.YPN8Qw.mb8Z-9rfNWk0yDBedu8FjAHwzvk')

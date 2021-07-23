import discord
from discord.ext import commands


async def scan_games(client):
    for member in client.get_all_members():
        if member:
            if member.game is None:
                return
            else:
                print(member.name, member.id, member.game)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun online.")
        # self.client.loop.create_task(scan_games(self.client))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "family" in message.content.lower():
            await message.reply("Did you say family? Nothing is stronger than family.")
        if "familie" in message.content.lower():
            await message.reply("Did you say family? Nothing is stronger than family.")

    # Commands
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.command()
    async def say(self, ctx, *, message: str):
        """Make the client say whatever you want it to say"""
        await ctx.send(message)



    @commands.command()
    async def ping(self, ctx):
        ctx.send("Pong!")


def setup(client):
    client.add_cog(Fun(client))

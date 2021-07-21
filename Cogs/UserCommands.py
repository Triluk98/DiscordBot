from shlex import join

import discord
from discord.ext import commands
import asyncio


async def status_task(self):
    await self.client.change_presence(activity=discord.Game("Kys"), status=discord.Status.online)
    await asyncio.sleep(10)


def is_not_pinned(msg):
    return not msg.pinned


class UserCommands(commands.Cog):

    def __init__(self, client2):
        self.client = client2

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("User Commands ready.")
        self.client.loop.create_task(status_task(self))

    # Commands
    @commands.command()
    async def userinfo(self, message, *, arg):
        member = discord.utils.find(lambda m: m.name == arg, message.guild.members)
        await message.channel.send(member)
        if member:
            embed = discord.Embed(title="Userinfo for {}".format(member.name),
                                  description="You are a sick bastard {}".format(member.mention),
                                  color=0x22a7f0)
            embed.add_field(name="Server joined", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"),
                            inline=True)
            embed.add_field(name="Discord joined", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
                            inline=True)
            roles = ""
            for role in member.roles:
                if not role.is_default():
                    roles += "{} \r\n".format(role.mention)
            if roles:
                embed.add_field(name="Roles", value=roles, inline=True)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="Gz.")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction(":PepeOkSign:802680979420479549")

    @commands.command()
    async def userhelp(self, message):
        await message.channel.send("PyBot Commands: To be continued...\r\n")


def setup(client):
    client.add_cog(UserCommands(client))
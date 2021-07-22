import discord
from discord.ext import commands
import asyncio


async def status_task(self):
    await self.client.change_presence(activity=discord.Game("Kys"), status=discord.Status.online)
    await asyncio.sleep(10)


def is_not_pinned(msg):
    return not msg.pinned


class UserCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("UserCommands online.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("User Commands ready.")
        self.client.loop.create_task(status_task(self))

    # Commands
    @commands.command()
    async def userinfo(self, message, *, arg):
        """Prints information about specific user (Parameter: user)"""
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
    async def serverinfo(self, ctx):
        """Prints information about the server (no parameters)"""
        server_name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
        owner = str(ctx.guild.owner)
        guild_id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels

        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Server Information for:\n" + server_name,
            description="Description:\n " + description,
            color=discord.Color.dark_green()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=True)
        embed.add_field(name='Highest role', value=ctx.guild.roles[-2], inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.add_field(name='Number of roles', value=str(role_count), inline=True)
        embed.add_field(name='Number of channels', value=str(channels), inline=True)
        embed.add_field(name='Number of categories', value=str(categories), inline=True)
        embed.add_field(name='Bots:', value=(', '.join(list_of_bots)))
        embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'),
                        inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def createinvite(self, ctx):
        """Creates an instant invite link (no parameters)"""
        link = await ctx.channel.create_invite(max_age=300)
        await ctx.send("Here is an instant invite to your server: " + str(link))

    # Error Handling
    @userinfo.error
    async def userinfo_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User] missing.")


def setup(client):
    client.add_cog(UserCommands(client))

import discord
from discord.abc import Messageable
from discord.ext import commands

channel_id = 867811753399812146
message = "Wähle deine Rollen!"

embed = discord.Embed(title="{}".format(message),color=0x22a7f0)
embed.add_field(name="Männlich", value="<:male:867852681234087997>", inline=False)
embed.add_field(name="Weiblich", value="<:female:867852705930543114>", inline=False)
embed.add_field(name=chr(173), value=chr(173), inline=False)
embed.add_field(name="League of Legends", value="<:LoL:867825143959126076>", inline=False)
embed.add_field(name="Diablo III", value="<:Diablo3:867820698147881010>", inline=False)
embed.add_field(name="Diablo IV", value="<:Diablo4:867820885637333034>", inline=False)
embed.add_field(name="Diablo II Resurrected", value="<:Diablo2Res:867825461957361684>", inline=False)
embed.add_field(name="Battlefield 2042", value="<:bf2042:867820515451469835>", inline=False)
embed.add_field(name="Path of Exile", value="<:PoE:867825215463751730>", inline=False)
embed.add_field(name="Afk Arena", value="<:afkarena:867825308128116736>", inline=False)
embed.add_field(name=chr(173), value=chr(173), inline=False)
embed.add_field(name="Python", value="<:Python:867851896974082068>", inline=False)
embed.add_field(name="C#", value="<:c_:867852430255718401>", inline=False)
embed.add_field(name="Java", value="<:java:867853663330107443>", inline=False)
embed.add_field(name="C++", value="<:cpp:867852403435896912>", inline=False)
embed.add_field(name="C", value="<:c_:867852384704790559>", inline=False)
embed.add_field(name="Javascript", value="<:js:867852353546092575>", inline=False)
embed.add_field(name="HTML/CSS", value="<:htmlcss:867852333563117598>", inline=False)

reactions = [":male:867852681234087997", ":female:867852705930543114", ":LoL:867825143959126076",
             ":Diablo3:867820698147881010", ":Diablo4:867820885637333034", ":Diablo2Res:867825461957361684",
             ":PoE:867825215463751730", ":afkarena:867825308128116736", ":bf2042:867820515451469835",
             ":Python:867851896974082068", ":c_:867852430255718401", ":cpp:867852403435896912", ":c_:867852384704790559",
             ":java:867853663330107443", ":js:867852353546092575", ":htmlcss:867852333563117598"]


async def del_msg(client):
    channel = client.get_channel(channel_id)
    messages = []
    number = int(5)

    async for x in Messageable.history(channel, limit=number):
        messages.append(x)
    for msg in messages:
        await msg.delete()


async def get_role_id(role_name):
    switcher = {
        "PoE": 802671934348197898,
        "LoL": 802664354423635989,
    }
    return switcher.get(role_name, "Invalid Role Name")


class RoleSelection(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("RoleSelection online.")
        await del_msg(self.client)
        channel = self.client.get_channel(channel_id)
        msg = await channel.send(embed=embed)
        # add all reactions to message
        for reaction in reactions:
            await msg.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # if wrong channel
        if reaction.message.channel.id != channel_id:
            return

        # if author is bot
        if reaction.message.author.bot:
            return

        # general roles
        if str(reaction.emoji) == "<:male:867852681234087997>":
            male = discord.utils.get(user.guild.roles, name="Male")
            await user.add_roles(male)
        if str(reaction.emoji) == "<:female:867852705930543114>":
            female = discord.utils.get(user.guild.roles, name="Female")
            await user.add_roles(female)

        # gaming roles
        if str(reaction.emoji) == "<:LoL:867825143959126076>":
            league = discord.utils.get(user.guild.roles, name="LoL")
            await user.add_roles(league)
        if str(reaction.emoji) == "<:Diablo3:867820698147881010>":
            diablo3 = discord.utils.get(user.guild.roles, name="Diablo3")
            await user.add_roles(diablo3)
        if str(reaction.emoji) == "<:Diablo4:867820885637333034>":
            diablo4 = discord.utils.get(user.guild.roles, name="Diablo4")
            await user.add_roles(diablo4)
        if str(reaction.emoji) == "<:Diablo2Res:867825461957361684>":
            diablo2r = discord.utils.get(user.guild.roles, name="Diablo2Resurrected")
            await user.add_roles(diablo2r)
        if str(reaction.emoji) == "<:PoE:867825215463751730>":
            poe = discord.utils.get(user.guild.roles, name="PoE")
            await user.add_roles(poe)
        if str(reaction.emoji) == "<:afkarena:867825308128116736>":
            afkarena = discord.utils.get(user.guild.roles, name="AfkArena")
            await user.add_roles(afkarena)
        if str(reaction.emoji) == "<:bf2042:867820515451469835>":
            bf2042 = discord.utils.get(user.guild.roles, name="Battlefield 2042")
            await user.add_roles(bf2042)

        # coding roles
        if str(reaction.emoji) == "<:Python:867851896974082068>":
            python = discord.utils.get(user.guild.roles, name="Python")
            await user.add_roles(python)
        if str(reaction.emoji) == "<:c_:867852430255718401>":
            csharp = discord.utils.get(user.guild.roles, name="C#")
            await user.add_roles(csharp)
        if str(reaction.emoji) == "<:cpp:867852403435896912>":
            cpp = discord.utils.get(user.guild.roles, name="C++")
            await user.add_roles(cpp)
        if str(reaction.emoji) == "<:c_:867852384704790559>":
            c = discord.utils.get(user.guild.roles, name="C")
            await user.add_roles(c)
        if str(reaction.emoji) == "<:java:867853663330107443>":
            java = discord.utils.get(user.guild.roles, name="Java")
            await user.add_roles(java)
        if str(reaction.emoji) == "<:js:867852353546092575>":
            js = discord.utils.get(user.guild.roles, name="Javascript")
            await user.add_roles(js)
        if str(reaction.emoji) == "<:htmlcss:867852333563117598>":
            htmlcss = discord.utils.get(user.guild.roles, name="HTML/CSS")
            await user.add_roles(htmlcss)

    @commands.command()
    async def remove_role(self, ctx, user: discord.Member, role):
        print("hallo???")
        print(user.display_name)
        print(role)
        role_to_remove = discord.utils.get(ctx.guild, name=role)
        await user.remove_roles(user, role_to_remove)
        await self.client.send("The Role {} has been removed from your user.".format(role))


def setup(client):
    client.add_cog(RoleSelection(client))

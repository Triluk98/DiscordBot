from discord.ext import commands
import asyncio


async def clear_file():
    while True:
        with open("Cogs/spam_detect.txt", "r+") as file:
            file.truncate(0)
        await asyncio.sleep(3600)


class AntiSpam(commands.Cog):

    def __int__(self, client2):
        self.client = client2

    @commands.Cog.listener()
    async def on_ready(self):
        print("AntiSpam running.")
        await clear_file()

    @commands.Cog.listener()
    async def on_message(self, message):
        counter = 0
        with open("Cogs/spam_detect.txt", "r+") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            file.writelines(f"{str(message.author.id)}\n")
            if counter > 8:
                await message.guild.ban(message.author, reason="Spam")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)
                await message.channel.send("User {} got kicked from the Server. Reason: Spam".format(message.author))
                await clear_file()


def setup(client):
    client.add_cog(AntiSpam(client))
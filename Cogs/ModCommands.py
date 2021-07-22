import discord
from discord.ext import commands


def is_not_pinned(msg):
    return not msg.pinned


def get_user(message, user):
    try:
        member = message.mentions[0]
    except message.mentions[0] is None:
        member = message.guild.get_member_named(user)
    if not member:
        try:
            member = message.guild.get_member(int(user))
        except ValueError:
            pass
    if not member:
        return None
    return member


class ModCommands(commands.Cog):

    def __int__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("ModCommands online.")

    # Commands
    @commands.command()
    async def clear(self, message, arg):
        if message.author.permissions_in(message.channel).manage_messages:
            if arg.isdigit():
                count = int(arg) + 1
                deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                await message.channel.send("{} Messages deleted.".format(len(deleted) - 1))
            else:
                await message.channel.send("Clear command: No number provided.")
        else:
            await message.channel.send("Clear command: No permission.")

    @commands.command()
    async def kick(self, ctx, user, *, reason=""):
        """Kicks a user"""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.kick(reason=reason)
                return_msg = "Kicked user '{}'".format(user.mention)
                if reason:
                    return_msg += " for reason '{}'".format(reason)
                return_msg += "."
                await ctx.send(return_msg)
            except discord.Forbidden:
                await ctx.send("Could not kick user, no permissions.")
        else:
            return await ctx.send("Could not find user.")

    @commands.command()
    async def hackban(self, ctx, user_id: int):
        """Bans a user outside of the server."""
        author = ctx.message.author
        guild = author.guild

        user = guild.get_member(user_id)
        if user is not None:
            return await ctx.invoke(self.ban, user=user)

        try:
            await self.client.http.ban(user_id, guild.id, 0)
            await ctx.send("Banned user: {}".format(user_id))
        except discord.NotFound:
            await ctx.send("Invalid user ID.")
        except discord.errors.Forbidden:
            await ctx.send("Not enough permissions.")

    @commands.command()
    async def ban(self, ctx, user, *, reason=""):
        """Bans a user."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                return_msg = "Banned user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.send(return_msg)
            except discord.Forbidden:
                await ctx.send('Could not ban user. Not enough permissions.')
        else:
            return await ctx.send('Could not find user.')

    @commands.command()
    async def softban(self, ctx, user, *, reason=""):
        """Bans and unbans a user."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                await ctx.guild.unban(user)
                return_msg = "Banned and unbanned user `{}`".format(user.name)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.send(return_msg)
            except discord.Forbidden:
                await ctx.send("Not enough permissions.")
        else:
            return await ctx.channel.send("User not found.")

    @commands.command()
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send("Unbanned user {}.".format(user.mention))

    @commands.command()
    async def mute(self, ctx, *, user: str):
        """Chat mutes a user."""
        if ctx.invoked_subcommand is None:
            user = get_user(ctx.message, user)
            if user and user != self.client.user:
                failed = []
                channel_length = 0
                for channel in ctx.message.guild.channels:
                    if type(channel) != discord.channel.TextChannel:
                        continue
                    overwrites = channel.overwrites_for(user)
                    overwrites.send_messages = False
                    channel_length += 1
                    try:
                        await channel.set_permissions(user, overwrite=overwrites)
                    except discord.Forbidden:
                        failed.append(channel)
                if failed and len(failed) < channel_length:
                    await ctx.send("Muted user in {}/{} channels: {}".format(
                        channel_length - len(failed), channel_length, user.mention))
                elif failed:
                    await ctx.send("Not enough permissions.")
                else:
                    await ctx.send("Muted user: {}".format(user.mention))
            else:
                await ctx.send("User not found.")

    @commands.command()
    async def unmute(self, ctx, *, user: str):
        """Unmutes a user."""
        if ctx.invoked_subcommand is None:
            user = get_user(ctx.message, user)
            if user:
                failed = []
                channel_length = 0
                for channel in ctx.message.guild.channels:
                    if type(channel) != discord.channel.TextChannel:
                        continue
                    overwrites = channel.overwrites_for(user)
                    overwrites.send_messages = None
                    channel_length += 1
                    is_empty = self.client.are_overwrites_empty(overwrites)
                    try:
                        if not is_empty:
                            await channel.set_permissions(user, overwrite=overwrites)
                        else:
                            await channel.set_permissions(user, overwrite=None)
                        await channel.set_permissions(user, overwrite=overwrites)
                    except discord.Forbidden:
                        failed.append(channel)
                if failed and len(failed) < channel_length:
                    await ctx.message.edit(content=self.client.bot_prefix + "Unmuted user in {}/{} channels: {}".format(
                        channel_length - len(failed), channel_length, user.mention))
                elif failed:
                    await ctx.message.edit(
                        content=self.client.bot_prefix + "Failed to unmute user. Not enough permissions.")
                else:
                    await ctx.message.edit(content=self.client.bot_prefix + 'Unmuted user: %s' % user.mention)
            else:
                await ctx.message.edit(content=self.client.bot_prefix + 'Could not find user.')

    # Error Handling
    @clear.error
    async def clear_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [Message Count] missing.")

    @kick.error
    async def kick_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User] missing.")

    @hackban.error
    async def hackban_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User ID] missing.")

    @ban.error
    async def ban_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User] missing.")

    @softban.error
    async def softban_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User] missing.")

    @unban.error
    async def unban_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User ID] missing.")

    @mute.error
    async def mute_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User] missing.")

    @unmute.error
    async def unmute_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [User] missing.")


def setup(client):
    client.add_cog(ModCommands(client))

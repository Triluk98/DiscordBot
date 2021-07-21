import discord
from discord.ext import commands


def is_not_pinned(msg):
    return not msg.pinned


def get_user(message, user):
    try:
        member = message.mentions[0]
    except:
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

    @commands.Cog.listener()
    async def on_ready(self):
        print("ModCommands ready.")

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

    @clear.error
    async def clear_error(self, message, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await message.send("Argument [Message Count] missing.")


    @commands.command()
    async def kick(self, ctx, user, *, reason=""):
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.kick(reason=reason)
                return_msg = "Kicked user '{}'".format(user.mention)
                if reason:
                    return_msg += " for reason '{}'".format(reason)
                return_msg += "."
                await ctx.message.edit(content=self.client.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content=self.client.bot_prefix + "Could not kick user, no permissions.")
        else:
            return await ctx.message.edit(content=self.client.bot_prefix + "Could not find user.")


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
            await ctx.message.edit(content=self.client.bot_prefix + 'Banned user: %s' % user_id)
        except discord.NotFound:
            await ctx.message.edit(content=self.client.bot_prefix + 'Could not find user. '
                                                                 'Invalid user ID was provided.')
        except discord.errors.Forbidden:
            await ctx.message.edit(content=self.client.bot_prefix + 'Could not ban user. Not enough permissions.')


    @commands.command()
    async def ban(self, ctx, user, *, reason=""):
        """Bans a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                return_msg = "Banned user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.message.edit(content=self.client.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content=self.client.bot_prefix + 'Could not ban user. Not enough permissions.')
        else:
            return await ctx.message.edit(content=self.client.bot_prefix + 'Could not find user.')

    @commands.command()
    async def softban(self, ctx, user, *, reason=""):
        """Bans and unbans a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                await ctx.guild.unban(user)
                return_msg = "Banned and unbanned user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.message.edit(content=self.client.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content=self.client.bot_prefix + 'Could not softban user. Not enough permissions.')
        else:
            return await ctx.message.edit(content=self.client.bot_prefix + 'Could not find user.')

    @commands.command()
    async def mute(self, ctx, *, user: str):
        """Chat mutes a user (if you have the permission)."""
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
                    await ctx.message.edit(content=self.client.bot_prefix + "Muted user in {}/{} channels: {}".format(
                        channel_length - len(failed), channel_length, user.mention))
                elif failed:
                    await ctx.message.edit(content=self.client.bot_prefix + "Failed to mute user. Not enough permissions.")
                else:
                    await ctx.message.edit(content=self.client.bot_prefix + 'Muted user: %s' % user.mention)
            else:
                await ctx.message.edit(content=self.client.bot_prefix + 'Could not find user.')

    @commands.command()
    async def unmute(self, ctx, *, user: str):
        """Unmutes a user (if you have the permission)."""
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


def setup(client):
    client.add_cog(ModCommands(client))
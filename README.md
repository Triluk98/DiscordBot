# DiscordBot

Small Discord.py bot inlcuding some Cogs with commands to organize your discord server or just return information.

## Featured Cogs
* Mod Commands
* User Commands
* Anti Spam
* Role Selection

# Usage
Antispam consists of a looped event listener which will store the User ID in the txt file "spam_detect" for each message send.
If the amount of one user's ID exceeds 10 then user will be softbanned, the txt file will be cleared every minute.

## Mod Commands
8 commands which help your moderators to control your discord server and intervene when encountering misbehaving members.
Parameters will be stated with []

* .clear [n]        - clears n + 1 (command itself) amount of messages in the current channel
* .kick [user]      - kicks the specified user from your server
* .hackban [user]   - bans a user outside of your server
* .ban [user]       - bans the specified user
* .softban [user]   - bans and unbans the user
* .unban [user]     - unbans the user
* .mute [user]      - mutes the specified user
* .unmute [user]    - unmutes the specified user

## User Commands

* userinfo [user]   - outputs information about the specified user, must be a guild member
* serverinfo        - prints information about your discord server
* createinvite      - creates an instant invite link in current channel

## Role Selection
Custom emotes and roles need to be added beforehand or adapted in sourcecode.
Specifiy desired channel by replacing channel_id in Cog.
Bot then posts an embed in this channel with all emojis which are connected to an specific role.
If user reacts on the message with one of those emojis, the role will be added.

## API Reference
* [Discord.py API Reference](https://discordpy.readthedocs.io/en/stable/api.html)

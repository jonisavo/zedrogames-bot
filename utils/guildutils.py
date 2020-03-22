import discord


async def get_text_channels(guild):
    channel_list = []
    # Fetch all text channels
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            channel_list.append(channel)
    return channel_list

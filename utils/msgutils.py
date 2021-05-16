from discord import DMChannel, MessageType
import asyncio


async def read_index_reply(context, array):
    def msg_check(msg):
        if not isinstance(msg.channel,
                          DMChannel) and msg.author is context.author:
            return False
        try:
            index = int(msg.content)
        except ValueError:
            return False
        if index < 0 or index >= len(array):
            return False
        return True

    try:
        message = await context.bot.wait_for('message',
                                             timeout=30.0,
                                             check=msg_check)
    except asyncio.TimeoutError:
        dm = context.author.dm_channel
        await dm.send("The query timed out.")
        return None
    else:
        return int(message.content)


def can_respond(message):
    return message.guild is None or (
        not message.author.bot and message.type == MessageType.default
        and message.channel.permissions_for(message.guild.me).send_messages)

import asyncio
import discord
from discord.ext import commands

from utils import guildutils, msgutils


class BaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def no_help(self, ctx):
        """In the triple-A games industry, no one can hear you scream."""
        # Delete the received command message
        await self.bot.delete_message(ctx.message)
        # Send a nice message
        await ctx.author.create_dm()
        dm = ctx.author.dm_channel
        todd_file = discord.File("assets/todd.png", filename="TODD.png")
        await dm.send("In the triple-A games industry, no one can hear you scream", file=todd_file)

    @commands.command(name='message')
    @commands.guild_only()
    @commands.is_owner()
    async def configure_message(self, ctx):
        """Allows the owner to send a custom message to any text channel
        of the guild the command was called in."""
        # Delete the received command message
        await self.bot.delete_message(ctx.message)
        channels = await guildutils.get_text_channels(ctx.guild)
        await ctx.author.create_dm()
        dm = ctx.author.dm_channel
        # If there are no text channels to send messages into, return
        if len(channels) == 0:
            dm.send(
                ("Hey there. You tried to send a message, but there aren't any "
                 f"text channels in {ctx.guild.name} to send it into.")
            )
            return
        # Otherwise let the user choose which channel their message should be sent to
        dm_text = (f"Beep. Boop. You're about to send a message to {ctx.guild.name}. "
                   "Select which channel you wish to send the message into.")
        for channel in channels:
            dm_text += f"\n{channels.index(channel)}: #{channel.name}"
        await dm.send(dm_text)
        # read_index_reply starts a query with a 30 second timer. If it expires, None is returned.
        selected_index = await msgutils.read_index_reply(ctx, channels)
        if selected_index is None:
            return
        selected_channel = channels[selected_index]
        await dm.send(f"You chose #{selected_channel.name} as the output channel.")
        await dm.send(f"Write any message, and it will be sent to #{selected_channel.name}. You have five minutes.")
        # Write a message for the bot to send
        try:
            message = await self.bot.wait_for('message', timeout=300.0, check=lambda msg:
            msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel))
        except asyncio.TimeoutError:
            await dm.send("The query timed out.")
            return

        # TODO get attachments to work
        # msg_files = []
        # for attachment in message.attachments:
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(attachment.url) as resp:
        #             buffer = BytesIO(await resp.read())
        #     file = discord.File(buffer, filename=attachment.filename, spoiler=attachment.is_spoiler())
        #     msg_files.append(file)
        # if len(msg_files) == 0:
        #     msg_files = None

        # At the moment, disallow sending empty messages
        if len(message.content) == 0:
            dm.send("You tried to send an empty message!")
            return
        # Ask for confirmation
        await dm.send(content=message.content, tts=message.tts)
        await dm.send(f"Send this message to #{selected_channel.name}? Y/N")
        try:
            confirmation = await self.bot.wait_for('message', timeout=30.0, check=lambda msg:
                                    msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel) and
                                    (msg.content.lower().startswith("y") or msg.content.lower().startswith("n")))
        except asyncio.TimeoutError:
            await dm.send("The query timed out.")
            return
        # If the user declined, return
        if confirmation.content.lower().startswith("n"):
            await dm.send("The operation was cancelled.")
            return
        # Attempt to send the message to the chosen channel
        try:
            await selected_channel.send(content=message.content, tts=message.tts)
        except discord.Forbidden:
            await dm.send("I could not send the message (error code 403: Forbidden). Do I have the necessary permissions?")
        except discord.HTTPException as e:
            await dm.send(f"I could not send the message (error code {e.status}: {e.text})")
        else:
            await dm.send("The message was sent.")
            print(f"A message was sent to {ctx.guild.name}>#{selected_channel.name} by {ctx.author}")


def setup(bot):
    bot.add_cog(BaseCommands(bot))


def teardown(bot):
    bot.remove_cog("BaseCommands")

import os
import asyncio
import random
from utils import msgutils, paasutils

import discord
from discord.ext import commands


class ZEDROGAMES(commands.Bot):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)
        self.paas_guild = None
        # These three commands are always there and can not be removed
        self.add_command(add_extension_command)
        self.add_command(remove_extension_command)
        self.add_command(list_extensions_command)

    async def on_ready(self):
        # Set the activity
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game("PokéMMOn 0.3.2"))
        # List all guilds the bot is connected into
        if len(self.guilds) == 0:
            print(
                f"{self.user} is connected to Discord, but isn't connected to a guild."
            )
        else:
            print(f"{self.user} is connected to the following guild(s):")
            paas_guild = os.environ.get("PAAS_GUILD")
            for guild in self.guilds:
                guildtxt = ""
                if paas_guild is not None and guild.id == int(paas_guild):
                    # If the PAAS guild is found, its ID is saved
                    self.paas_guild = guild
                    guildtxt += "[PAAS GUILD] "
                guildtxt += f"{guild.name} (id: {guild.id})"
                print(guildtxt)

    async def on_message(self, message):
        # The bot doesn't react to its own messages or system messages
        if not msgutils.can_respond(message):
            return
        # Process commands
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            pass
        else:
            await self.generate_error(context, exception)

    async def write_message(self, destination, message):
        """Creates a new task for writing a message."""
        self.loop.create_task(self.message_creation(destination, message))

    async def message_creation(self, destination, message):
        """Makes the bot look like it's typing a message."""
        async with destination.typing():
            if isinstance(message, str):
                msglength = len(message)
            else:
                msglength = len(message.content)
            await asyncio.sleep(
                max(
                    min(
                        msglength / 6 + random.randint(0, 4) -
                        random.randint(0, 4), 20), 3))
            await destination.send(message)

    async def delete_message(self, message):
        """Attempts to delete the given message. Has some enhanced error management. Returns whether
        sending the message was successful."""
        # Can't delete a private message or a system message
        if message.guild is None or message.type is not discord.MessageType.default:
            return False
        try:
            await message.delete()
        except discord.Forbidden:
            print(
                f"Deleting message {message.id} at {message.guild}>#{message.channel} failed: Forbidden. "
                "Is the manage_messages permission missing?")
            return False
        except discord.NotFound:
            print(
                f"Deleting message {message.id} at {message.guild}>#{message.channel} failed: Not Found. "
                "Has the message been deleted already?")
            return False
        except discord.HTTPException as e:
            print(
                f"Deleting message {message.id} at {message.guild}>#{message.channel} failed with code {e.status}: "
                f"{e.text}")
            return False
        else:
            return True

    async def generate_error(self, ctx, error):
        """Prints out a custom error message using the given context and exception."""
        msg = ""
        if ctx.guild:
            server_address = f"{ctx.guild.name}>#{ctx.message.channel}"
        else:
            server_address = "Direct Messages"
        msg += f"{ctx.prefix}{ctx.command} error: attempted call from {server_address}>{ctx.author}"
        if isinstance(error, commands.NoPrivateMessage):
            msg += "\n > Called from a private message context"
        elif isinstance(error, commands.PrivateMessageOnly):
            msg += "\n > Called from a guild context"
        elif isinstance(error, commands.NotOwner):
            msg += "\n > Author is not the owner"
        elif isinstance(error, paasutils.CheckFailure_PAASGuild):
            msg += "\n > Function was not called from the PAAS guild"
        else:
            msg += f"\n > {error}"
        print(msg)


@commands.command(name="addext")
@commands.is_owner()
async def add_extension_command(ctx, ext_name):
    """Loads the given extension."""
    await ctx.bot.delete_message(ctx.message)
    if ext_name in ctx.bot.extensions:
        await ctx.author.send("That extension is already loaded.")
        return
    try:
        ctx.bot.load_extension(ext_name)
    except commands.ExtensionNotFound:
        await ctx.author.send("That extension does not exist.")
    except commands.NoEntryPointError:
        await ctx.author.send(
            "That extension does not have a setup() function.")
    except commands.ExtensionFailed as e:
        await ctx.author.send(f"An exception was raised: {e.original}")
    else:
        await ctx.author.send("The extension was loaded.")
        print(f"Loaded extension {ext_name}")


@commands.command(name="rmext")
@commands.is_owner()
async def remove_extension_command(ctx, ext_name):
    """Unloads the given extension."""
    await ctx.bot.delete_message(ctx.message)
    if ext_name not in ctx.bot.extensions:
        await ctx.author.send("That extension is not loaded.")
        return
    ctx.bot.unload_extension(ext_name)
    await ctx.author.send("The extension was unloaded.")
    print(f"Unloaded extension {ext_name}")


@commands.command(name="listext")
@commands.is_owner()
async def list_extensions_command(ctx):
    """Sends a DM containing a list of all active extensions."""
    await ctx.bot.delete_message(ctx.message)
    await ctx.author.send(
        "Here's all currently active extensions: ```\n{}```".format("\n".join(
            ctx.bot.extensions.keys())))


@add_extension_command.error
async def add_ext_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.author.send(
            "An extension name must be given. !addext [EXTENSION NAME]")
    else:
        await ctx.bot.generate_error(ctx, error)


@remove_extension_command.error
async def remove_ext_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.author.send(
            "An extension name must be given. !rmext [EXTENSION NAME]")
    else:
        await ctx.bot.generate_error(ctx, error)

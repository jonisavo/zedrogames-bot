from discord.ext import commands


class CheckFailure_PAASGuild(commands.CheckFailure):
    pass


# Returns whether a command was given in the specified guild.
def in_paas_guild():

    async def predicate(ctx):
        if ctx.guild and ctx.bot.paas_guild and ctx.guild.id == ctx.bot.paas_guild.id:
            return True
        else:
            raise CheckFailure_PAASGuild()

    return commands.check(predicate)

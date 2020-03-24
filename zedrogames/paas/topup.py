import random
from utils import paasutils

from discord.ext import commands


class PAAS_Topup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='topup')
    @paasutils.in_paas_guild()
    async def topup_command(self, ctx):
        # Delete the command
        await self.bot.delete_message(ctx.message)
        # Send the user a top-up code
        code = await self.generate_code(ctx.author.id)
        await ctx.author.send(f"Greetings, {ctx.author.name}. Here's your unique top-up code:\n `` {code} ``")

    async def generate_code(self, givenseed):
        if givenseed is not None:
            random.seed(a=givenseed)
        code = ""
        code += random.choice(["a", "k", "p", "8"])
        code += random.choice(["7", "-", "b", "1"])
        code += random.choice(["u", "9", "0", "_"])
        code += random.choice(["8", "a", "q", "="])
        code += random.choice(["z", "3", "$", "#"])
        code += random.choice(["<", "/", "i", "h"])
        code += random.choice(["w", "t", "/", "%"])
        code += random.choice(["f", "b", "e", "s"])
        random.seed(a=None)
        return code


def setup(bot):
    bot.add_cog(PAAS_Topup(bot))


def teardown(bot):
    bot.remove_cog("TopupCommand")

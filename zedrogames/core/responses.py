import random
from utils import msgutils, quotes

from discord import ChannelType
from discord.ext import commands


class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Has a chance to respond to messages with a random quote."""
        if not msgutils.can_respond(message):
            return
        # Small chance to respond to messages
        if message.channel.type == ChannelType.private:
            if random.randint(0, 60) == 0:
                await self.bot.write_message(message.channel, random.choice(quotes.annoyed_quotes))
        else:
            if random.randint(0, 90) == 0:
                await self.bot.write_message(message.channel, random.choice(quotes.normal_quotes))

    @commands.command(name='quote')
    @commands.is_owner()
    async def test_quotes(self, ctx):
        """Says a random quote."""
        await self.bot.delete_message(ctx.message)
        await self.bot.write_message(ctx, random.choice(quotes.normal_quotes))


def setup(bot):
    bot.add_cog(Responses(bot))


def teardown(bot):
    bot.remove_cog("Responses")

from utils import msgutils

import discord
from discord.ext import commands


class ToddReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 16 times the triggers
        self.triggers = [
            "todd", "howard", "fallout", "skyrim", "morrowind", "oblivion",
            "elder scrolls", "bethesda", "horse armor", "it just works",
            "times the detail", "76", "premium membership", "loot box",
            "denuvo", "drm"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if not msgutils.can_respond(message):
            return
        # React with :todd: if the PAAS guild exists
        if self.bot.paas_guild is not None:
            for item in self.triggers:
                if item in message.content.lower():
                    todd_emote = discord.utils.get(self.bot.paas_guild.emojis,
                                                   name='todd')
                    if todd_emote is None:
                        return
                    await message.add_reaction(todd_emote)
                    break


def setup(bot):
    bot.add_cog(ToddReaction(bot))


def teardown(bot):
    bot.remove_cog("ToddReaction")

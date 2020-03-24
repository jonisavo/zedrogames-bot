from discord.ext import commands
from utils import paasutils


class PAAS_Download(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='download')
    @commands.guild_only()
    @paasutils.in_paas_guild()
    async def download_game(self, ctx):
        print(f"!download called by {ctx.guild.name}>#{ctx.message.channel}>{ctx.author}")
        # Delete the received command message
        await self.bot.delete_message(ctx.message)
        # Send a message to whoever asked for a download
        await ctx.author.send(
            (f"Hello, {ctx.author.name}! Thank you for your interest in PokéMMOn, the most ambitious fangame ever "
             "created. We're still working on the game, so we don't have a download to give you just yet. Please stay tuned!")
        )


def setup(bot):
    bot.add_cog(PAAS_Download(bot))


def teardown(bot):
    bot.remove_cog("DownloadCommand")

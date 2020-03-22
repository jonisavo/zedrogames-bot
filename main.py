import os

from zedrogames.bot import ZEDROGAMES
from utils import extutils

if os.environ.get("DISCORD_TOKEN") is None:
    raise RuntimeError("Fatal error: the DISCORD_TOKEN environment variable has not been set!")

if os.environ.get("OWNER_ID") is None:
    raise RuntimeError("Fatal error: the OWNER_ID environment variable has not been set!")

bot = ZEDROGAMES(command_prefix="!", help_command=None, owner_id=int(os.environ.get("OWNER_ID")))

extutils.load_all_extensions(bot)

print("Connecting...")
bot.run(os.environ.get("DISCORD_TOKEN"))

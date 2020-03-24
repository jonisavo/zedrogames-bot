import random
from utils import msgutils

from discord.ext import commands

sections = {
    "Settings": {
        "length": 364,
    },
    "PField_Field": {
        "length": 1425
    },
    "PokeBattle_Trainer": {
        "length": 298
    },
    "PItem_Items": {
        "length": 895
    },
    "PScreen_PauseMenu": {
        "length": 323
    },
    "PScreen_Load": {
        "length": 876
    },
    "PScreen_Save": {
        "length": 205
    },
    "PScreen_Options": {
        "length": 796
    },
    "PScreen_PokemonStorage": {
        "length": 1948
    },
    "Updates": {
        "length": 452
    },
    "Users": {
        "length": 496
    },
    "Achievements": {
        "length": 1799
    },
    "Store_Items": {
        "length": 1768
    },
    "Pokemon Summon": {
        "length": 1015
    },
    "Direct Messages": {
        "length": 1127
    },
    "Public Events": {
        "length": 730
    },
    "Main": {
        "length": 70
    }
}


class RGSSError:
    def __init__(self):
        self.error_type = random.choice([
            "NoMethodError",
            "SyntaxError"
        ])
        self.section = ""
        self.line = 1
        self.text = None
        if self.error_type == "NoMethodError":
            self.generate_nomethoderror()
        elif self.error_type == "SyntaxError":
            self.generate_syntaxerror()
        else:
            self.generate_syntaxerror()

    def generate_nomethoderror(self):
        """Generates the text for a NoMethodError."""
        self.section, self.line = self.generate_location()
        method = random.choice([
            "name",
            "level",
            "length",
            "update",
            "push",
            "bitmap",
            "dispose",
            "clear"
            "each",
            "keys"
        ])
        classname = random.choice([
            "nil:NilClass",
            f"{random.randint(0,100)}:Fixnum",
            "true:TrueClass",
            "false:FalseClass"
        ])
        self.text = f"undefined method '{method}' for {classname}"

    def generate_syntaxerror(self):
        """Generates the text for a SyntaxError."""
        self.section, self.line = self.generate_location()
        if random.randint(0,3) == 0:
            self.line = sections.get(self.section).get("length")

    def generate_location(self):
        """Generates a random location for the RGSS error."""
        section = random.choice(list(sections.keys()))
        line = random.randint(1, sections.get(section).get("length")+1)
        return section, line

    def get(self):
        """Creates the error report."""
        text = f"Script '{self.section}' line {self.line}: {self.error_type} occurred."
        if self.text:
            text += f"\n\n{self.text}"
        text += "\n\n" + random.choice([
            "Any help? -Zed",
            "help please -garis",
            "Uhh... what does this mean? -Zedrovas",
            "Can someone help? -Zed",
            "wtf why is this not working -garis",
            "any help.... ? i fucking hate rpg maker -garis",
            "Does anyone here know Ruby? -Zedrovas",
            "GOD WHO THE FUCK DESIGNED THIS GOD FORSAKEN EGNINE -g",
            "i hate my life",
            "Help needed! -Zedrovas",
            "uh"
        ])
        return text


class RGSSTechSupport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not msgutils.can_respond(message):
            return
        if random.randint(0, 200) == 0:
            await self.bot.write_message(message.channel, RGSSError().get())

    @commands.command(name='rgsserror')
    @commands.is_owner()
    async def test_error(self, ctx):
        """Sends a random RGSS error report to the current channel."""
        await self.bot.delete_message(ctx.message)
        await self.bot.write_message(ctx, RGSSError().get())


def setup(bot):
    bot.add_cog(RGSSTechSupport(bot))


def teardown(bot):
    bot.remove_cog("RGSSTechSupport")

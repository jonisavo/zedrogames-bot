import os
from discord.ext import commands


def load_all_extensions(bot, path="./zedrogames"):
    for currentpath, folders, files in os.walk(path):
        for file in files:
            if file.startswith("__") or file.endswith(
                    ".pyc") or currentpath == path:
                continue
            # I'm still learning Python so this may be tough to look at, sorry folks.
            # This code transforms the cog file paths (e.g. ./zedrogames\core\base.py)
            # to a dot-separated format (e.g. zedrogames.core.base)
            ext_name = get_extension_from_path(os.path.join(currentpath, file))
            if ext_name not in bot.extensions:
                try:
                    print(f"Loading extension {ext_name}")
                    bot.load_extension(ext_name)
                except commands.ExtensionNotFound:
                    print(" > Failure: extension was not found")
                except commands.NoEntryPointError:
                    print(
                        " > Failure: extension does not have a setup() function"
                    )
                except commands.ExtensionFailed as e:
                    print(f" > Failure: an exception was raised: {e.original}")


# This function is unused (for now?)
def find_extension(name, path="./zedrogames"):
    for currentpath, folders, files in os.walk(path):
        for file in files:
            if file.startswith("__") or file.endswith(
                    ".pyc") or currentpath == path:
                continue
            ext_path = os.path.join(currentpath, file.replace(".py", ""))\
                .replace("\\", "/")\
                .split("/")
            ext_path.pop(0)
            if ext_path[len(ext_path)] == name:
                return ".".join(ext_path)
    return None


def get_extension_from_path(path):
    if path.endswith(".py"):
        path = path[:-3]
    path = path.replace("\\", "/").split("/")
    path.pop(0)
    return ".".join(path)

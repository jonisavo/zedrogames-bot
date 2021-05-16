import random
from utils import msgutils

import discord
from discord.ext import commands


class Microtransactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.remove_locked_roles(self.bot.get_all_members())

    @commands.Cog.listener()
    async def on_message(self, message):
        if not msgutils.can_respond(message):
            return
        # Generate a random integer from 0 to 300
        if random.randint(0, 300) == 0 and message.guild is not None:
            await self.lock_account(message.author)

    @commands.command(name='purgelocks')
    @commands.is_owner()
    async def purge_locks_command(self, ctx):
        """Removes all locked roles from everyone."""
        # Delete the command
        await self.bot.delete_message(ctx.message)
        # Send a confirmation
        await ctx.author.send("We're about to purge all locked roles.")
        # Attempt to purge locked roles
        await self.remove_locked_roles(self.bot.get_all_members())

    @commands.command(name="lockme")
    @commands.guild_only()
    @commands.is_owner()
    async def test_lock(self, ctx):
        """Locks your account (for testing purposes)."""
        await self.bot.delete_message(ctx.message)
        await self.lock_account(ctx.author)

    async def lock_account(self, member):
        """Locks the given account."""
        # Stop if adding the locked role failed
        if await self.add_locked_role(member,
                                      "Microtransaction time!") is False:
            return
        # Send a dm and wait for a reaction
        await member.send(f"""\
**CONGRATULATIONS!**
You've been chosen to happily pay a small microtransaction to stay in
> {member.guild.name}
You will not be able to send messages in this server until you pay.
Pay your microtransaction by reacting to this message with 💰
We hope you feel a strong sense of pride and accomplishment.
                    """)

        def reaction_check(reaction, user):
            return user == member and str(reaction.emoji) == '💰'

        await self.bot.wait_for('reaction_add', check=reaction_check)
        await self.remove_locked_role(member, "The microtransaction was paid.")
        await self.bot.write_message(
            member.dm_channel,
            f"Thank you for your purchase, {member.name}! You may now continue existing."
        )

    async def add_locked_role(self, member, specified_reason=None):
        """Adds the locked role to the specified member. A reason can be specified."""
        locked_role = discord.utils.get(member.guild.roles, name='locked')
        print(f"Giving locked role to {member.guild.name}>{member}")
        # Return if the locked role doesn't exist or the author already has it
        if locked_role is None or locked_role in member.roles:
            print(
                " > Failed: locked role does not exist or author already has it"
            )
            return False
        # Attempt to give the author the locked role
        try:
            await member.add_roles(locked_role, reason=specified_reason)
        except discord.Forbidden:
            print(
                " > Failed: Forbidden. Is the manage_roles permission missing?"
            )
            return False
        except discord.HTTPException as e:
            print(f" > Failed - status code {e.status}: {e.text}")
            return False
        else:
            return True

    async def remove_locked_role(self, member, specified_reason=None):
        """Remoes the locked role from the specified member. A reason can be specified."""
        locked_role = discord.utils.get(member.guild.roles, name='locked')
        print(f"Removing locked role from {member.guild.name}>{member}")
        # Return if the locked role doesn't exist or the author doesn't have it
        if locked_role is None or locked_role not in member.roles:
            print(
                " > Failed: locked role does not exist or author does not have it"
            )
            return False
        # Attempt to remove the locked role
        try:
            await member.remove_roles(locked_role, reason=specified_reason)
        except discord.Forbidden:
            print(
                " > Failed: Forbidden. Is the manage_roles permission missing?"
            )
            return False
        except discord.HTTPException as e:
            print(f" > Failed - status code {e.status}: {e.text}")
            return False
        else:
            return True

    async def remove_locked_roles(self, members):
        """Removes the locked role from all specified members."""
        for member in members:
            locked_role = discord.utils.get(member.guild.roles, name='locked')
            if locked_role is not None and locked_role in member.roles:
                print(f"Removing locked role at: {member.guild.name}>{member}")
                try:
                    await member.remove_roles(
                        locked_role, reason="Removing multiple locked roles.")
                except discord.Forbidden:
                    print(" > Forbidden: is manage_roles permission missing?")
                except discord.HTTPException as e:
                    print(
                        f" > HTTPException - Status Code {e.status}: {e.text}")


def setup(bot):
    bot.add_cog(Microtransactions(bot))


def teardown(bot):
    bot.remove_cog("Microtransactions")

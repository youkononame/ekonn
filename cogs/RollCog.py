import random
import discord
from discord.ext import commands


class RollCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    roll_group = discord.app_commands.Group(
        name="roll", description="One-dimensional games of chance"
    )

    @roll_group.command(
        name="flip", description="Flip a coin to double (or lose) your wager"
    )
    @discord.app_commands.choices(
        choice=[
            discord.app_commands.Choice(name="Heads", value="heads"),
            discord.app_commands.Choice(name="Tails", value="tails"),
        ]
    )
    async def flip(
        self,
        interaction: discord.Interaction,
        choice: discord.app_commands.Choice[str],
        wager: int,
    ):
        if wager < 1:
            await interaction.response.send_message(
                embed=discord.Embed(title="You must bet at least $1")
            )
            return

        profile = self.bot.get_cog("UsersCog").profiles[interaction.user.id]
        if wager > profile.balance:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can not bet more than your balance",
                    description=f"Your current balance is ${profile.balance}",
                )
            )
            return

        correct = random.randint(1, 2) == 1 if choice.value == "heads" else random.randint(1, 2) == 2
        profile.balance += wager if correct else -wager
        profile.update()

        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"{"You guessed correctly!" if correct else "Better luck next time..."}",
                description=f"Your new balance is ${profile.balance}",
            )
        )


async def setup(bot):
    await bot.add_cog(RollCog(bot))

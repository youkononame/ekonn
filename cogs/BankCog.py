import core.mongo
import cogs.UsersCog
import discord
from discord.ext import commands


class BankCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    bank_group = discord.app_commands.Group(
        name="bank", description="Manage your money"
    )

    @bank_group.command(name="balance", description="View your bank account balance")
    async def balance(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        member = interaction.user if member is None else member
        if member.bot:
            await interaction.response.send_message(
                embed=discord.Embed(title="Robots don't use banks, silly goose")
            )
            return

        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"{"Your" if member == interaction.user else member.display_name + "'s"} balance",
                description=f"${self.bot.get_cog("UsersCog").profiles[member.id].balance}",
            )
        )

    @bank_group.command(name="daily", description="Claim a daily reward of $100")
    @discord.app_commands.checks.cooldown(1, 60 * 60 * 24)
    async def daily(self, interaction: discord.Interaction):
        profile = self.bot.get_cog("UsersCog").profiles[interaction.user.id]
        profile.balance += 100
        profile.update()

        await interaction.response.send_message(
            embed=discord.Embed(
                title="$100 reward claimed",
                description=f"Your new balance is ${profile.balance}",
            )
        )


async def setup(bot):
    await bot.add_cog(BankCog(bot))

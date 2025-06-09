import os
import datetime
import asyncio
import dotenv
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        try:
            print(f"Synced {len(await self.tree.sync())} commands")
        except Exception as exception:
            print(f"Failed to sync command tree. Error: {exception}")


intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix=None, intents=intents, help_command=None)


@bot.tree.error
async def on_error(
    interaction: discord.Interaction, error: discord.app_commands.AppCommandError
):
    match type(error):
        case discord.app_commands.NoPrivateMessage:
            await interaction.response.send_message(
                "This command does not work in private messages.",
                ephemeral=True,
            )
        case discord.app_commands.MissingRole | discord.app_commands.MissingAnyRole:
            await interaction.response.send_message(
                "You are missing the required role(s) to run this command.",
                ephemeral=True,
            )
        case discord.app_commands.MissingPermissions:
            await interaction.response.send_message(
                "You are missing the required permission(s) to run this command.",
                ephemeral=True,
            )
        case discord.app_commands.CommandOnCooldown:
            tdelta = datetime.timedelta(seconds=error.retry_after)
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            f = "{days}d, {hours}h, {minutes}m, and {seconds}s"

            await interaction.response.send_message(
                f"This command is on cooldown! Try again in {f.format(**d)}.",
                ephemeral=True,
            )
        case _:
            await interaction.response.send_message(
                "An unknown error occured in the processing of your command.",
                ephemeral=True,
            )
            print(
                f"Error occured in the processing of the command {interaction.command}. Error: {error}"
            )


COGS_DIRECTORY = "./cogs"


async def load_cogs():
    if not os.path.isdir(COGS_DIRECTORY):
        print("Cogs directory is missing!")
        return

    for filename in os.listdir(COGS_DIRECTORY):
        if filename.endswith(".py"):
            extension_name = f"cogs.{filename[:-3]}"

            try:
                await bot.load_extension(extension_name)
                print("Synced cog " + extension_name)
            except Exception as exception:
                print(f"Failed to load extension {extension_name}. Error: {exception}")

if __name__ == "__main__":
    dotenv.load_dotenv(dotenv.find_dotenv())

    asyncio.run(load_cogs())
    bot.run(os.getenv("BOT_TOKEN"))

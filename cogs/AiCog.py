import requests
import json
import discord
from discord.ext import commands


class AiCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @discord.app_commands.command(
        name="llm", description="Chat with a large language model"
    )
    async def llm(self, interaction: discord.Interaction, prompt: str):
        ai_response = requests.post(
            "https://ai.hackclub.com/chat/completions",
            headers={"Content-Type": "application/json"},
            json={"messages": [{"role": "user", "content": prompt}]},
        ).json()["choices"][0]["message"]["content"]

        await interaction.response.send_message(ai_response)


async def setup(bot):
    await bot.add_cog(AiCog(bot))

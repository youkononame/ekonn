import core.mongo
import core.profile
import discord
from discord.ext import commands


class UsersCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.profiles = {}

    @commands.Cog.listener()
    async def on_ready(self):
        db = core.mongo.collection.find({})
        existing_profiles = {
            profile_document["user_id"]: core.profile.create_profile(profile_document)
            for profile_document in db
        }

        for member in self.bot.get_all_members():
            if member.bot:
                continue

            if member.id in existing_profiles.keys():
                continue

            self.profiles[member.id] = core.profile.Profile(member.id).update()

        self.profiles.update(existing_profiles)
        print(f"{len(self.profiles)} users loaded, {len(existing_profiles)} prexisted")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        profiles[member.id] = core.profile.Profile(member.id).update()


async def setup(bot):
    await bot.add_cog(UsersCog(bot))

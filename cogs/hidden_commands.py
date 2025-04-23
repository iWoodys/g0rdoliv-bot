from discord.ext import commands

OWNER_ID = 1100168924978499595  # Cambialo por tu ID real

class HiddenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def setup(self, bot):
        await bot.add_cog(HiddenCommands(bot))


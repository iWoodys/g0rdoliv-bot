import discord
from discord.ext import commands
from discord import app_commands
import config

OWNER_ID = 1100168924978499595  # Reemplázalo con tu ID real

class HiddenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cerrar", description="Cerrar sesión | Solo el propietario del BOT puede utilizar este comando, por favor ignorá este comando.")
    async def cerrar(self, interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ No tienes permiso para usar este comando.", ephemeral=True)
            return

        await interaction.response.send_message("👋 Cerrando sesión y saliendo del servidor...", ephemeral=True)
        await interaction.guild.leave()

async def setup(bot):
    await bot.add_cog(HiddenCommands(bot))


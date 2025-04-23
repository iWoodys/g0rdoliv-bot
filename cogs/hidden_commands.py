from discord.ext import commands
from discord import app_commands, Interaction

class HiddenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    OWNER_ID = 1100168924978499595  # 🔁 Cambialo por tu ID real de Discord

    @app_commands.command(name="cerrar", description="Comando oculto para cerrar el bot (solo dueño)")
    async def cerrar(self, interaction: Interaction):
        if interaction.user.id != self.OWNER_ID:
            await interaction.response.send_message("❌ No tenés permiso para usar este comando.", ephemeral=True)
            return

        await interaction.response.send_message("👋 Cerrando sesión y saliendo del servidor...", ephemeral=True)
        await interaction.guild.leave()  # Sale del servidor donde se ejecuta

async def setup(bot):
    cog = HiddenCommands(bot)
    bot.tree.add_command(cog.cerrar)  # No usamos sync para que quede invisible
    await bot.add_cog(cog)

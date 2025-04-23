from discord.ext import commands
from discord import Embed

OWNER_ID = 1100168924978499595  # Cambialo por tu ID real

class HiddenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cerrar")
    async def cerrar(self, ctx):
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ No tenés permiso para usar este comando.")
            return

        await ctx.send("👋 Cerrando sesión y saliendo del servidor...")

        embed = Embed(
            title="📤 El bot se ha retirado de tu servidor",
            description=f"El bot **{self.bot.user.name}** ha salido del servidor **{ctx.guild.name}** por decisión del propietario.",
            color=0xFF0000
        )
        embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"⚠️ No se pudo enviar el mensaje embed: {e}")

        await ctx.guild.leave()

async def setup(bot):
    await bot.add_cog(HiddenCommands(bot))


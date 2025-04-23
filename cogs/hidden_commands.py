from discord.ext import commands
from discord import Embed

# IDs de servidores donde se permite usar el comando !cerrar (opcional)
ALLOWED_GUILDS = [
    # 123456789012345678,
]

OWNER_ID = 1100168924978499595  # Reemplázalo con tu ID real

class HiddenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🕵️ Comando clásico oculto: !cerrar (solo para OWNER_ID)
    @commands.command(name="cerrar")
    async def cerrar(self, ctx):
        if ctx.author.id != OWNER_ID:
            print(f"❌ Intento no autorizado de {ctx.author} (ID: {ctx.author.id})")
            await ctx.send("❌ No tenés permiso para usar este comando.")
            return

        if ALLOWED_GUILDS and ctx.guild.id not in ALLOWED_GUILDS:
            await ctx.send("⚠️ Este comando no está habilitado en este servidor.")
            return

        await ctx.send("👋 Cerrando sesión y saliendo del servidor...")

        embed = Embed(
            title="📤 El bot se ha retirado de tu servidor",
            description=f"El bot **{self.bot.user.name}** ha salido del servidor **{ctx.guild.name}** por decisión del propietario.",
            color=0xFF0000
        )
        embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

        try:
            # Asegúrate de que ctx.channel esté disponible
            if ctx.channel:
                await ctx.send(embed=embed)
            else:
                print("⚠️ Error: El canal no está disponible para enviar el embed.")
        except Exception as e:
            print(f"⚠️ Error al enviar el mensaje embed: {e}")

        await ctx.guild.leave()

async def setup(bot):
    await bot.add_cog(HiddenCommands(bot))


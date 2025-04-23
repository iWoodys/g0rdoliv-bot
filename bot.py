import discord
from discord.ext import commands
from discord import Embed
import config
from keep_alive import keep_alive
import asyncio

# Inicia el servidor Flask apenas arranca el bot
keep_alive()

# IDs de servidores donde se permite usar el comando !cerrar
ALLOWED_GUILDS = [
    # Agregá acá el ID del servidor donde está permitido, si querés limitarlo (opcional)
    # 123456789012345678
]

OWNER_ID = 1100168924978499595  # Reemplazá con tu ID real

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    activity = discord.Activity(type=discord.ActivityType.watching, name="2.941.013 players in Warzone")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print("📜 Servidores donde está el bot:")
    for guild in bot.guilds:
        print(f"👉 {guild.name} (ID: {guild.id})")

    # Si querés que se salga automáticamente de ciertos servers
    IGNORED_GUILDS = []
    for guild in bot.guilds:
        if guild.id in IGNORED_GUILDS:
            print(f"🚪 Saliendo del servidor: {guild.name}")
            await guild.leave()

    try:
        synced = await bot.tree.sync()
        print(f"🌐 Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

# 🕵️ Comando secreto: !cerrar (solo para el owner, opcionalmente restringido por servidor)
@bot.command(name="cerrar")
async def cerrar(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ No tenés permiso para usar este comando.")
        return

    if ALLOWED_GUILDS and ctx.guild.id not in ALLOWED_GUILDS:
        await ctx.send("⚠️ Este comando no está habilitado en este servidor.")
        return

    await ctx.send("👋 Cerrando sesión y saliendo del servidor...")

    embed = Embed(
        title="📤 El bot se ha retirado de tu servidor",
        description=f"El bot **{bot.user.name}** ha salido del servidor **{ctx.guild.name}** por decisión del propietario.",
        color=0xFF0000
    )
    embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

    try:
        await ctx.send(embed=embed)
        print(f"📨 Mensaje enviado al canal del servidor: {ctx.channel.name}")
    except Exception as e:
        print(f"⚠️ No se pudo enviar el mensaje al canal: {e}")

    await ctx.guild.leave()

async def main():
    await bot.load_extension("cogs.warzone")
    await bot.load_extension("cogs.hidden_commands")  # Si tenés más comandos ocultos, los cargás acá
    await bot.start(config.TOKEN)

asyncio.run(main())

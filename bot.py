import discord
from discord.ext import commands
from discord import Embed
import config
from keep_alive import keep_alive
import asyncio

# Inicia el servidor Flask apenas arranca el bot
keep_alive()

# Lista de IDs de servidores a ignorar (cuando quieras, ponelos acá)
IGNORED_GUILDS = [
    # 123456789012345678,
    # 234567890123456789
]

# ⚠️ Reemplazá este ID con tu ID real de Discord
OWNER_ID = 1100168924978499595

intents = discord.Intents.default()
intents.messages = True  # Asegúrate de que el bot tiene acceso para leer y escribir mensajes
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    activity = discord.Activity(type=discord.ActivityType.watching, name="2.941.013 players in Warzone")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print("📜 Servidores donde está el bot:")
    for guild in bot.guilds:
        print(f"👉 {guild.name} (ID: {guild.id})")

    for guild in bot.guilds:
        if guild.id in IGNORED_GUILDS:
            print(f"🚪 Saliendo del servidor: {guild.name}")
            await guild.leave()

    try:
        synced = await bot.tree.sync()
        print(f"🌐 Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

# 🕵️ Comando con prefijo: !cerrar
@bot.command(name="cerrar")
async def cerrar(ctx):
    # Verificar si el usuario es el dueño del bot
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ No tenés permiso para usar este comando.")
        return

    await ctx.send("👋 Cerrando sesión y saliendo del servidor...")

    # Enviar un embed al canal del servidor donde se ejecutó el comando
    embed = Embed(
        title="📤 El bot se ha retirado de tu servidor",
        description=f"El bot **{bot.user.name}** ha salido del servidor **{ctx.guild.name}** por decisión del propietario del bot.",
        color=0xFF0000
    )
    embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

    # Enviar el embed al canal donde se ejecutó el comando
    try:
        await ctx.send(embed=embed)
        print(f"📨 Mensaje enviado al canal del servidor: {ctx.channel.name}")
    except Exception as e:
        print(f"⚠️ No se pudo enviar el mensaje al canal: {e}")

    # 🚪 Salir del servidor
    await ctx.guild.leave()

async def main():
    await bot.load_extension("cogs.warzone")
    await bot.start(config.TOKEN)

asyncio.run(main())

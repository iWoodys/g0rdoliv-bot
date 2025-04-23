import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
import config
from keep_alive import keep_alive
import asyncio

# Inicia el servidor Flask apenas arranca el bot
keep_alive()

# Lista de IDs de servidores a ignorar
IGNORED_GUILDS = [
    # 123456789012345678,
    # 234567890123456789
]

# Tu ID como dueño del bot
OWNER_ID = 1100168924978499595

# Intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

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
        # Limpieza de comandos viejos y sincronización
        await bot.tree.clear_commands(guild=None)  # Limpia los globales
        synced = await bot.tree.sync()
        print(f"🧹 Comandos antiguos eliminados y nuevos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Error al limpiar/sincronizar comandos: {e}")

# ✅ Comando /cerrar eliminado — ahora solo usás /off desde cogs.warzone

# Inicia el bot
async def main():
    try:
        await bot.load_extension("cogs.warzone")  # Carga el cog correctamente
    except Exception as e:
        print(f"❌ Error al cargar la extensión warzone: {e}")
    await bot.start(config.TOKEN)

asyncio.run(main())

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

intents = discord.Intents.default()
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
        print(f"🌐 Comandos sincronizados: {len(synced)} slash commands activos")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

async def main():
    await bot.load_extension("cogs.warzone")
    await bot.start(config.TOKEN)

asyncio.run(main())

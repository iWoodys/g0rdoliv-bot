import discord
from discord.ext import commands
import config
from keep_alive import keep_alive
import asyncio

# Inicia el servidor Flask apenas arranca el bot
keep_alive()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

async def main():
    await bot.load_extension("cogs.warzone")
    await bot.start(config.TOKEN)

asyncio.run(main())


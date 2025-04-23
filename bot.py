import discord
from discord.ext import commands
import config
from keep_alive import keep_alive
import asyncio

# Inicia el servidor Flask apenas arranca el bot
keep_alive()

# IDs de servidores donde se permite usar el comando !cerrar (opcional)
ALLOWED_GUILDS = [
    # 123456789012345678,
]

OWNER_ID = 1100168924978499595  # Reemplazalo con tu ID real

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=config.APPLICATION_ID  # Necesario para que funcionen slash commands
)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    # Sincroniza los comandos para asegurarse de que estén disponibles
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Comandos slash sincronizados: {len(synced)}")
        for cmd in synced:
            print(f"🔹 /{cmd.name}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

    activity = discord.Activity(type=discord.ActivityType.watching, name="2.941.013 players in Warzone")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print("📜 Servidores donde está el bot:")
    for guild in bot.guilds:
        print(f"👉 {guild.name} (ID: {guild.id})")

    IGNORED_GUILDS = []
    for guild in bot.guilds:
        if guild.id in IGNORED_GUILDS:
            print(f"🚪 Saliendo del servidor: {guild.name}")
            await guild.leave()

async def main():
    await bot.load_extension("cogs.warzone")
    await bot.load_extension("cogs.hidden_commands")  # Descomentada para cargar el cog de comandos ocultos
    await bot.start(config.TOKEN)

asyncio.run(main())

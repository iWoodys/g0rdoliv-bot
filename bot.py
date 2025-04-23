import discord
from discord.ext import commands
from discord import Embed
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
intents.guilds = True  # Necesario para recibir eventos sobre servidores

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

@bot.event
async def on_guild_join(guild):
    # El bot buscará el canal de "spams" en el servidor
    channel = discord.utils.get(guild.text_channels, name="spams")

    # Si no encuentra el canal de spams, usa el primer canal de texto disponible
    if not channel:
        channel = guild.text_channels[0]

    embed = Embed(
        title="¡Bienvenido al servidor!",
        description="Gracias por invitarme a tu servidor. Soy un bot para gestionar loadouts de Warzone. Aquí te dejo las instrucciones:",
        color=0x006400  # Verde oscuro
    )
    embed.add_field(name="Comandos", value="Usa los comandos slash para interactuar conmigo. Ejemplo: `/warzone` para ver los loadouts.")
    embed.add_field(name="¿Cómo agregar un loadout?", value="Para agregar un loadout, usa el comando `/add_loadout` (requiere permisos de administrador).")
    embed.add_field(name="¿Cómo editar un loadout?", value="Usa el comando `/edit_loadout` para editar un loadout existente.")
    embed.add_field(name="¿Cómo eliminar un loadout?", value="Usa el comando `/delete_loadout` para eliminar un loadout.")
    embed.add_field(name="Dato Importante", value="Para eliminar un accesorio del loadout utiliza /edit_loadout, busca la categoría a eliminar y escribes: NO. Ejemplo: /edit_loadout Stock: NO.")

    # Enviar el mensaje embed al canal de "spams" o el primer canal de texto
    await channel.send(embed=embed)

async def main():
    await bot.load_extension("cogs.warzone")
    await bot.load_extension("cogs.hidden_commands")  # Descomentada para cargar el cog de comandos ocultos
    await bot.start(config.TOKEN)

asyncio.run(main())

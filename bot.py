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
        print(f"🌐 Comandos slash sincronizados: {len(synced)}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

# Comando SLASH /cerrar, solo lo podés usar vos
@bot.tree.command(name="cerrar", description="Cerrar el bot (solo para el dueño)")
async def cerrar(interaction: Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ No tenés permiso para usar este comando.", ephemeral=True)
        return

    await interaction.response.send_message("👋 Cerrando sesión y saliendo del servidor...", ephemeral=True)

    embed = Embed(
        title="📤 El bot se ha retirado de tu servidor",
        description=f"El bot **{bot.user.name}** ha salido del servidor **{interaction.guild.name}** por decisión del propietario del bot.",
        color=0xFF0000
    )
    embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

    try:
        await interaction.channel.send(embed=embed)
        print(f"📨 Mensaje enviado al canal: {interaction.channel.name}")
    except Exception as e:
        print(f"⚠️ No se pudo enviar mensaje al canal: {e}")

    await interaction.guild.leave()

# Inicia el bot
async def main():
    try:
        await bot.load_extension("warzone")  # ✅ Corregido (antes decía "cogs.warzone")
    except Exception as e:
        print(f"❌ Error al cargar la extensión warzone: {e}")
    await bot.start(config.TOKEN)

asyncio.run(main())


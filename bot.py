import discord
from discord.ext import commands
from discord import Embed, app_commands
import config
from keep_alive import keep_alive
import asyncio

OWNER_ID = 1100168924978499595  # Reemplázalo con tu ID real

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Comandos slash sincronizados: {len(synced)}")
        for cmd in synced:
            print(f"🔹 /{cmd.name}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

    activity = discord.Activity(type=discord.ActivityType.watching, name="2.941.013 players in Warzone")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels, name="spams") or guild.text_channels[0]

    embed = Embed(
        title="¡Bienvenido al servidor!",
        description="Gracias por invitarme. Usa los comandos slash para gestionar loadouts de Warzone.",
        color=0x006400
    )
    embed.add_field(name="Comandos", value="`/warzone`, `/add_loadout`, `/edit_loadout`, `/delete_loadout`")
    embed.add_field(name="Nota", value="Solo administradores pueden agregar o editar. El comando `/cerrar` es solo para el dueño del bot.")
    await channel.send(embed=embed)

@bot.tree.command(name="cerrar", description="Cerrar sesión y salir del servidor (solo propietario)")
async def cerrar(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ No tienes permiso para usar este comando.", ephemeral=True)
        return
    await interaction.response.send_message("👋 Cerrando sesión...", ephemeral=True)
    await interaction.guild.leave()

async def main():
    keep_alive()
    await bot.load_extension("cogs.warzone")
    await bot.start(config.TOKEN)

asyncio.run(main())

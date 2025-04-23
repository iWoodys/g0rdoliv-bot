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

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=config.APPLICATION_ID  # Necesario para que funcionen slash commands
)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

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

    try:
        synced = await bot.tree.sync()
        print(f"🌐 Comandos slash sincronizados: {len(synced)}")
        for cmd in synced:
            print(f"🔹 /{cmd.name}")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

# 🕵️ Comando clásico oculto: !cerrar (solo para OWNER_ID)
@bot.command(name="cerrar")
async def cerrar(ctx):
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
        description=f"El bot **{bot.user.name}** ha salido del servidor **{ctx.guild.name}** por decisión del propietario.",
        color=0xFF0000
    )
    embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

    try:
        await ctx.send(embed=embed)
        print(f"📨 Embed enviado en {ctx.channel.name}")
    except Exception as e:
        print(f"⚠️ Error al enviar embed: {e}")

    await ctx.guild.leave()

async def main():
    await bot.load_extension("cogs.warzone")
    # await bot.load_extension("cogs.hidden_commands")  # solo si tenés otros cogs secretos
    await bot.start(config.TOKEN)

asyncio.run(main())

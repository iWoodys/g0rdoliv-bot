from discord.ext import commands
from discord import app_commands, Interaction, Embed
from discord.ui import View
from views.weapon_buttons import WeaponButton
from database import save_loadout, get_loadouts, delete_loadout
from datetime import datetime

OWNER_ID = 1100168924978499595

class LoadoutView(View):
    def __init__(self, user_id, guild_id, loadouts):
        super().__init__(timeout=60)
        self.user_id = user_id

        for weapon in loadouts.keys():
            self.add_item(WeaponButton(label=weapon, user_id=user_id, guild_id=guild_id))

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.user_id

class Warzone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loadouts", description="Mostrar los loadouts de Warzone")
    async def loadouts(self, interaction: Interaction):
        guild_id = str(interaction.guild.id)
        loadouts = await get_loadouts(guild_id)

        if not loadouts:
            await interaction.response.send_message("⚠️ No hay loadouts guardados aún.", ephemeral=True)
            return

        embed = Embed(
            title="🎯 Loadouts de Warzone",
            description=f"**{interaction.user.display_name}**, seleccioná un arma para ver su configuración:",
            color=0xFF0000
        )
        view = LoadoutView(interaction.user.id, guild_id, loadouts)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="add_l", description="Agregar un loadout (solo admins)")
    @app_commands.describe(weapon_name="Nombre del arma", title="Título", image="URL de imagen")
    async def add_l(self, interaction: Interaction, weapon_name: str, title: str, image: str = ""):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los admins pueden usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        data = {
            "title": title,
            "attachments": {},  # Se puede expandir si querés más adelante
            "image": image,
            "timestamp": datetime.now().strftime("%d/%m/%y, %I:%M %p")
        }

        await save_loadout(guild_id, weapon_name, data)
        await interaction.response.send_message(f"✅ Loadout **{weapon_name}** agregado.", ephemeral=True)

    @app_commands.command(name="edit_l", description="Editar un loadout (solo admins)")
    @app_commands.describe(weapon_name="Nombre del arma", title="Nuevo título", image="Nueva imagen")
    async def edit_l(self, interaction: Interaction, weapon_name: str, title: str, image: str = ""):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los admins pueden usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        loadouts = await get_loadouts(guild_id)

        if weapon_name not in loadouts:
            await interaction.response.send_message(f"⚠️ No se encontró un loadout para **{weapon_name}**.", ephemeral=True)
            return

        loadouts[weapon_name]["title"] = title
        if image:
            loadouts[weapon_name]["image"] = image
        loadouts[weapon_name]["timestamp"] = datetime.now().strftime("%d/%m/%y, %I:%M %p")

        await save_loadout(guild_id, weapon_name, loadouts[weapon_name])
        await interaction.response.send_message(f"✅ Loadout de **{weapon_name}** actualizado.", ephemeral=True)

    @app_commands.command(name="del_l", description="Eliminar un loadout (solo admins)")
    @app_commands.describe(weapon_name="Nombre del arma")
    async def del_l(self, interaction: Interaction, weapon_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Solo los admins pueden usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        loadouts = await get_loadouts(guild_id)

        if weapon_name not in loadouts:
            await interaction.response.send_message(f"⚠️ No se encontró un loadout para **{weapon_name}**.", ephemeral=True)
            return

        await delete_loadout(guild_id, weapon_name)
        await interaction.response.send_message(f"🗑️ Loadout **{weapon_name}** eliminado.", ephemeral=True)

    @app_commands.command(name="off", description="Apagar el bot y salir del servidor (solo dueño)")
    async def off(self, interaction: Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Solo el dueño puede usar este comando.", ephemeral=True)
            return

        await interaction.response.send_message("👋 Cerrando sesión y saliendo del servidor...", ephemeral=True)

        embed = Embed(
            title="📤 El bot se ha retirado del servidor",
            description=f"El bot **{self.bot.user.name}** salió del servidor **{interaction.guild.name}**.",
            color=0xFF0000
        )
        embed.set_footer(text="Gracias por usar Warzone Loadouts Stream")

        try:
            await interaction.channel.send(embed=embed)
        except Exception as e:
            print(f"⚠️ Error al enviar mensaje al canal: {e}")

        await interaction.guild.leave()

async def setup(bot):
    await bot.add_cog(Warzone(bot))

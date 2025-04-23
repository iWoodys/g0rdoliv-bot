from discord.ext import commands
from discord import app_commands, Interaction, Embed
from discord.ui import View
from views.weapon_buttons import WeaponButton
from database import save_loadout, get_loadouts, delete_loadout
from datetime import datetime

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

        # Vincular comandos al árbol
        self.bot.tree.add_command(self.warzone)
        self.bot.tree.add_command(self.add_loadout)
        self.bot.tree.add_command(self.edit_loadout)
        self.bot.tree.add_command(self.delete_loadout)

    @app_commands.command(name="warzone", description="Mostrar las armas de Warzone")
    async def warzone(self, interaction: Interaction):
        guild_id = str(interaction.guild.id)
        loadouts = await get_loadouts(guild_id)

        embed = Embed(
            title="🎯 Loadouts de Warzone",
            description=f"**{interaction.user.display_name}** selecciona un arma para ver su configuración:",
            color=0xFF0000
        )
        view = LoadoutView(user_id=interaction.user.id, guild_id=guild_id, loadouts=loadouts)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="add_loadout", description="Agregar un nuevo loadout (solo admins)")
    @app_commands.describe(
        weapon_name="Nombre del arma",
        title="Título para mostrar",
        optic="Óptica",
        muzzle="Boca de cañón",
        barrel="Cañón",
        underbarrel="Bajo cañón",
        magazine="Cargador",
        rear_grip="Empuñadura trasera",
        stock="Culata",
        fire_mode="Mod. de fuego",
        image="URL de la imagen"
    )
    async def add_loadout(self, interaction: Interaction,
                          weapon_name: str,
                          title: str,
                          optic: str = None,
                          muzzle: str = None,
                          barrel: str = None,
                          underbarrel: str = None,
                          magazine: str = None,
                          rear_grip: str = None,
                          stock: str = None,
                          fire_mode: str = None,
                          image: str = None):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        attachments = {
            "Optic": optic, "Muzzle": muzzle, "Barrel": barrel, "Underbarrel": underbarrel,
            "Magazine": magazine, "Rear Grip": rear_grip, "Stocks": stock, "Fire Mods": fire_mode
        }
        attachments = {k: v for k, v in attachments.items() if v}

        data = {
            "title": title,
            "attachments": attachments,
            "image": image or "",
            "timestamp": datetime.now().strftime("%d/%m/%y, %I:%M %p")
        }

        await save_loadout(guild_id, weapon_name, data)
        await interaction.response.send_message(f"✅ Loadout para **{weapon_name}** agregado.", ephemeral=True)

    @app_commands.command(name="edit_loadout", description="Editar un loadout existente (solo admins)")
    @app_commands.describe(
        weapon_name="Nombre exacto del arma a editar",
        title="Título para mostrar",
        optic="Óptica", muzzle="Boca de cañón", barrel="Cañón", underbarrel="Bajo cañón",
        magazine="Cargador", rear_grip="Empuñadura trasera", stock="Culata",
        fire_mode="Mod. de fuego", image="URL de la imagen"
    )
    async def edit_loadout(self, interaction: Interaction,
                           weapon_name: str,
                           title: str,
                           optic: str = None, muzzle: str = None, barrel: str = None,
                           underbarrel: str = None, magazine: str = None,
                           rear_grip: str = None, stock: str = None,
                           fire_mode: str = None, image: str = None):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        loadouts = await get_loadouts(guild_id)

        if weapon_name not in loadouts:
            await interaction.response.send_message(f"⚠️ No se encontró ningún loadout llamado '{weapon_name}'.", ephemeral=True)
            return

        data = loadouts[weapon_name]
        attachments = data.get("attachments", {})

        updates = {
            "Optic": optic, "Muzzle": muzzle, "Barrel": barrel, "Underbarrel": underbarrel,
            "Magazine": magazine, "Rear Grip": rear_grip, "Stocks": stock, "Fire Mods": fire_mode,
        }

        for key, value in updates.items():
            if value:
                if value.strip().upper() == "NO":
                    attachments.pop(key, None)
                else:
                    attachments[key] = value.strip()

        data["title"] = title
        data["attachments"] = attachments
        if image:
            data["image"] = image
        data["timestamp"] = datetime.now().strftime("%d/%m/%y, %I:%M %p")

        await save_loadout(guild_id, weapon_name, data)
        await interaction.response.send_message(f"✅ Loadout de **{weapon_name}** actualizado.", ephemeral=True)

    @app_commands.command(name="delete_loadout", description="Eliminar un loadout por nombre (solo admins)")
    @app_commands.describe(weapon_name="Nombre del arma a eliminar")
    async def delete_loadout(self, interaction: Interaction, weapon_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)
        loadouts = await get_loadouts(guild_id)

        if weapon_name not in loadouts:
            await interaction.response.send_message(f"⚠️ No se encontró ningún loadout llamado '{weapon_name}'.", ephemeral=True)
            return

        await delete_loadout(guild_id, weapon_name)
        await interaction.response.send_message(f"✅ Loadout '{weapon_name}' eliminado correctamente.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Warzone(bot))

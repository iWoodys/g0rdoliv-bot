from discord.ext import commands
from discord import app_commands, Interaction, Embed
from discord.ui import View
from views.weapon_buttons import WeaponButton
import json
from datetime import datetime

def load_loadouts():
    with open("loadouts.json", "r") as f:
        return json.load(f)

def save_loadouts(data):
    with open("loadouts.json", "w") as f:
        json.dump(data, f, indent=4)

class LoadoutView(View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
        loadouts = load_loadouts()

        for weapon in loadouts.keys():
            self.add_item(WeaponButton(label=weapon, user_id=user_id))

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.user_id

class Warzone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warzone", description="Mostrar las armas de Warzone")
    async def warzone(self, interaction: Interaction):
        embed = Embed(
            title="🎯 Loadouts de Warzone",
            description=f"**{interaction.user.display_name}** selecciona un arma para ver su configuración:",
            color=0xFF0000
        )

        view = LoadoutView(user_id=interaction.user.id)
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

        loadouts = load_loadouts()

        attachments = {}
        if optic: attachments["Optic"] = optic
        if muzzle: attachments["Muzzle"] = muzzle
        if barrel: attachments["Barrel"] = barrel
        if underbarrel: attachments["Underbarrel"] = underbarrel
        if magazine: attachments["Magazine"] = magazine
        if rear_grip: attachments["Rear Grip"] = rear_grip
        if stock: attachments["Stocks"] = stock
        if fire_mode: attachments["Fire Mods"] = fire_mode

        loadouts[weapon_name] = {
            "title": title,
            "attachments": attachments,
            "image": image or "",
            "timestamp": datetime.now().strftime("%d/%m/%y, %I:%M %p")
        }

        save_loadouts(loadouts)
        await interaction.response.send_message(f"✅ Loadout para **{weapon_name}** agregado exitosamente.", ephemeral=True)

    @app_commands.command(name="edit_loadout", description="Editar un loadout existente (solo admins)")
    @app_commands.describe(
        weapon_name="Nombre exacto del arma a editar",
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
    async def edit_loadout(self, interaction: Interaction,
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

        loadouts = load_loadouts()

        if weapon_name not in loadouts:
            await interaction.response.send_message(f"⚠️ No se encontró ningún loadout llamado '{weapon_name}'.", ephemeral=True)
            return

        updates = {
            "Optic": optic,
            "Muzzle": muzzle,
            "Barrel": barrel,
            "Underbarrel": underbarrel,
            "Magazine": magazine,
            "Rear Grip": rear_grip,
            "Stocks": stock,
            "Fire Mods": fire_mode,
        }

        attachments = loadouts[weapon_name].get("attachments", {})

        for key, value in updates.items():
            if value:
                if value.strip().upper() == "NO":
                    attachments.pop(key, None)
                else:
                    attachments[key] = value.strip()

        loadouts[weapon_name]["title"] = title
        loadouts[weapon_name]["attachments"] = attachments
        if image:
            loadouts[weapon_name]["image"] = image
        loadouts[weapon_name]["timestamp"] = datetime.now().strftime("%d/%m/%y, %I:%M %p")

        save_loadouts(loadouts)
        await interaction.response.send_message(f"✅ Loadout de **{weapon_name}** actualizado exitosamente.", ephemeral=True)

    @app_commands.command(name="delete_loadout", description="Eliminar un loadout por nombre (solo admins)")
    @app_commands.describe(weapon_name="Nombre del arma a eliminar")
    async def delete_loadout(self, interaction: Interaction, weapon_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
            return

        loadouts = load_loadouts()
        if weapon_name not in loadouts:
            await interaction.response.send_message(f"⚠️ No se encontró ningún loadout llamado '{weapon_name}'.", ephemeral=True)
            return

        del loadouts[weapon_name]
        save_loadouts(loadouts)

        await interaction.response.send_message(f"✅ Loadout '{weapon_name}' eliminado correctamente.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Warzone(bot))

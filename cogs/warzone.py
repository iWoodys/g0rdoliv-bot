from discord.ext import commands
from discord import app_commands, Interaction, Embed
from discord.ui import View
from views.weapon_buttons import WeaponButton
import json
import os
from datetime import datetime

LOADOUTS_FILE = "loadouts.json"

def load_loadouts():
    if not os.path.exists(LOADOUTS_FILE):
        with open(LOADOUTS_FILE, "w") as f:
            json.dump({}, f)
    with open(LOADOUTS_FILE, "r") as f:
        return json.load(f)

def save_loadouts(data):
    with open(LOADOUTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class LoadoutView(View):
    def __init__(self, user_id, guild_id):
        super().__init__(timeout=60)
        self.user_id = user_id
        loadouts = load_loadouts()
        guild_loadouts = loadouts.get(guild_id, {})

        for weapon in guild_loadouts.keys():
            self.add_item(WeaponButton(label=weapon, user_id=user_id, guild_id=guild_id))  # ← cambio aplicado

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
        view = LoadoutView(user_id=interaction.user.id, guild_id=str(interaction.guild.id))
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
        guild_id = str(interaction.guild.id)

        if guild_id not in loadouts:
            loadouts[guild_id] = {}

        attachments = {}
        if optic: attachments["Optic"] = optic
        if muzzle: attachments["Muzzle"] = muzzle
        if barrel: attachments["Barrel"] = barrel
        if underbarrel: attachments["Underbarrel"] = underbarrel
        if magazine: attachments["Magazine"] = magazine
        if rear_grip: attachments["Rear Grip"] = rear_grip
        if stock: attachments["Stocks"] = stock
        if fire_mode: attachments["Fire Mods"] = fire_mode

        loadouts[guild_id][weapon_name] = {
            "title": title,
            "attachments": attachments,
            "image": image or "",
            "timestamp": datetime.now().strftime("%d/%m/%y, %I:%M %p")
        }

        save_loadouts(loadouts)
        await interaction.response.send_message(f"✅ Loadout para **{weapon_name}** agregado en este servidor.", ephemeral=True)

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
        guild_id = str(interaction.guild.id)

        if guild_id not in loadouts or weapon_name not in loadouts[guild_id]:
            await interaction.response.send_message(f"⚠️ No se encontró ningún loadout llamado '{weapon_name}' en este servidor.", ephemeral=True)
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

        attachments = loadouts[guild_id][weapon_name].get("attachments", {})

        for key, value in updates.items():
            if value:
                if value.strip().upper() == "NO":
                    attachments.pop(key, None)
                else:
                    attachments[key] = value.strip()

        loadouts[guild_id][weapon_name]["title"] = title
        loadouts[guild_id][weapon_name]["attachments"] = attachments
        if image:
            loadouts[guild_id][weapon_name]["image"] = image
        loadouts[guild_id][weapon_name]["timestamp"] = datetime.now().strftime("%d/%m/%y, %I:%M %p")

        save_loadouts(loadouts)
        await interaction.response.send_message(f"✅ Loadout de **{weapon_name}** actualizado.", ephemeral=True)

    @app_commands.command(name="delete_loadout", description="Eliminar un loadout por nombre (solo admins)")
    @app_commands.describe(weapon_name="Nombre del arma a eliminar")
    async def delete_loadout(self, interaction: Interaction, weapon_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
            return

        loadouts = load_loadouts()
        guild_id = str(interaction.guild.id)

        if guild_id not in loadouts or weapon_name not in loadouts[guild_id]:
            await interaction.response.send_message(f"⚠️ No se encontró ningún loadout llamado '{weapon_name}' en este servidor.", ephemeral=True)
            return

        del loadouts[guild_id][weapon_name]
        save_loadouts(loadouts)

        await interaction.response.send_message(f"✅ Loadout '{weapon_name}' eliminado correctamente.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Warzone(bot))

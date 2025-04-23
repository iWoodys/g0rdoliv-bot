from discord.ui import Button
from discord import ButtonStyle, Interaction
from views.loadout_embed import generate_weapon_embed

class WeaponButton(Button):
    def __init__(self, label, user_id, guild_id):
        # Asignamos un custom_id para que el botón funcione aunque se reinicie el bot
        super().__init__(label=label, style=ButtonStyle.primary, custom_id=f"loadout_{label}")
        self.user_id = user_id
        self.guild_id = guild_id

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ No puedes usar este botón.", ephemeral=True)
            return

        try:
            embed = generate_weapon_embed(self.guild_id, self.label)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            await interaction.response.send_message("❌ Error al mostrar el loadout.", ephemeral=True)


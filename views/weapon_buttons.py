from discord.ui import Button
from discord import ButtonStyle, Interaction
from views.loadout_embed import generate_weapon_embed

class WeaponButton(Button):
    def __init__(self, label, user_id):
        super().__init__(label=label, style=ButtonStyle.primary)
        self.user_id = user_id

    async def callback(self, interaction: Interaction):
        # Eliminamos la restricción para que todos los usuarios puedan ver el loadout
        embed = generate_weapon_embed(self.label)
        await interaction.response.send_message(embed=embed, ephemeral=False)


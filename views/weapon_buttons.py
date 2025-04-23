from discord.ui import Button
from discord import ButtonStyle, Interaction
from views.loadout_embed import generate_weapon_embed

class WeaponButton(Button):
    def __init__(self, label, user_id, guild_id):
        super().__init__(label=label, style=ButtonStyle.primary)
        self.user_id = user_id
        self.guild_id = guild_id

async def callback(self, interaction: Interaction):
    try:
        embed = generate_weapon_embed(self.guild_id, self.label)
        await interaction.response.send_message(embed=embed, ephemeral=False)
    except Exception as e:
        await interaction.response.send_message("❌ Este botón ya no es válido. Probá usar el comando de nuevo.", ephemeral=True)


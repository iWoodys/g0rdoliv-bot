import json
from discord.ui import Modal, TextInput
from discord import TextStyle, Interaction
from datetime import datetime

class AddLoadoutModal(Modal):
    def __init__(self):
        super().__init__(title="Agregar nuevo Loadout")

        self.weapon_name = TextInput(
            label="Nombre del arma",
            placeholder="Ej: AK74U"
        )
        self.attachments = TextInput(
            label="Accesorios (uno por línea)",
            style=TextStyle.paragraph,
            placeholder="Óptica: Reflex\nBoca de cañón: Compensator\n...",
            required=True
        )
        self.image = TextInput(
            label="URL de imagen (opcional)",
            required=False
        )

        self.add_item(self.weapon_name)
        self.add_item(self.attachments)
        self.add_item(self.image)

    async def on_submit(self, interaction: Interaction):
        # Procesar los accesorios a un diccionario
        lines = self.attachments.value.strip().splitlines()
        parsed_attachments = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                parsed_attachments[key.strip()] = value.strip()

        new_loadout = {
            self.weapon_name.value: {
                "title": self.weapon_name.value,
                "attachments": parsed_attachments,
                "image": self.image.value or "https://i.imgur.com/EZKWfuB.png",
                "timestamp": datetime.now().strftime("%d/%m/%y, %I:%M %p")
            }
        }

        with open("loadouts.json", "r") as f:
            data = json.load(f)

        data.update(new_loadout)

        with open("loadouts.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(
            f"✅ Loadout **{self.weapon_name.value}** agregado con éxito.",
            ephemeral=True
        )


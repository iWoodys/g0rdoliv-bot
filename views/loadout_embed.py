import json
from discord import Embed

def load_loadouts():
    with open("loadouts.json", "r") as f:
        return json.load(f)

def generate_weapon_embed(guild_id: str, weapon_name: str) -> Embed:
    loadouts = load_loadouts()
    data = loadouts[guild_id][weapon_name]

    embed = Embed(
        title=data["title"],
        color=0xFF0000
    )

    for slot, attachment in data["attachments"].items():
        embed.add_field(name=slot, value=attachment, inline=False)

    embed.set_image(url=data["image"])
    embed.set_footer(text=data["timestamp"])

    return embed


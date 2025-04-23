from discord import Embed
from database import get_loadouts

def generate_weapon_embed_sync(guild_id: str, weapon_name: str) -> Embed:
    # Esta función no es async, por eso usamos .stream() directamente
    from firebase_admin import firestore
    db = firestore.client()
    doc_ref = db.document(f"loadouts/{guild_id}_{weapon_name}")
    doc = doc_ref.get()
    
    if not doc.exists:
        raise ValueError(f"No se encontró el loadout '{weapon_name}' en este servidor.")

    data = doc.to_dict()

    embed = Embed(
        title=data["title"],
        color=0xFF0000
    )

    for slot, attachment in data["attachments"].items():
        embed.add_field(name=slot, value=attachment, inline=False)

    if data.get("image"):
        embed.set_image(url=data["image"])
    
    embed.set_footer(text=data["timestamp"])

    return embed



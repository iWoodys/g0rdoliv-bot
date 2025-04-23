import asyncio
from discord import Embed
from firebase_admin import firestore
from concurrent.futures import ThreadPoolExecutor

# Executor global para ejecutar funciones sincrónicas en un hilo separado
executor = ThreadPoolExecutor()

# Función asíncrona para envolver la consulta sincrónica de Firestore
async def generate_weapon_embed(guild_id: str, weapon_name: str) -> Embed:
    loop = asyncio.get_event_loop()
    # Ejecutamos la consulta Firestore en un hilo separado para no bloquear el hilo principal
    doc = await loop.run_in_executor(executor, fetch_loadout, guild_id, weapon_name)

    if not doc:
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

# Función sincrónica que realiza la consulta a Firestore
def fetch_loadout(guild_id: str, weapon_name: str):
    db = firestore.client()
    doc_ref = db.document(f"loadouts/{guild_id}_{weapon_name}")
    return doc_ref.get()



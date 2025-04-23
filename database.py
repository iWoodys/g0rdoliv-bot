import firebase_admin
from firebase_admin import credentials, firestore
import json

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("botdiscord-6a44b-firebase-adminsdk-fbsvc-f6b7234780.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Ya no se necesita init_db con Firestore

def doc_path(guild_id, weapon_name):
    return f"loadouts/{guild_id}_{weapon_name}"

async def save_loadout(guild_id, weapon_name, data):
    path = doc_path(guild_id, weapon_name)
    db.document(path).set(data)

async def get_loadouts(guild_id):
    loadouts_ref = db.collection("loadouts")
    docs = loadouts_ref.stream()
    result = {}
    for doc in docs:
        if doc.id.startswith(f"{guild_id}_"):
            weapon_name = doc.id.split("_", 1)[1]
            result[weapon_name] = doc.to_dict()
    return result

async def delete_loadout(guild_id, weapon_name):
    path = doc_path(guild_id, weapon_name)
    db.document(path).delete()


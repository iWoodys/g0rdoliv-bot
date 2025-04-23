import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Ruta donde Render guarda el Secret File
cred_path = "/etc/secrets/FIREBASE_CREDENTIALS"

if os.path.exists(cred_path):
    print("Credenciales encontradas en archivo secreto.")
    with open(cred_path, "r") as f:
        cred_dict = json.load(f)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
else:
    print("No se han encontrado credenciales.")
    raise ValueError("Las credenciales de Firebase no están disponibles.")
    
db = firestore.client()

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

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Obtener las credenciales desde la variable de entorno
cred_data = os.environ.get("FIREBASE_CREDENTIALS")

# Verificar si se obtuvieron las credenciales correctamente
if cred_data:
    print("Credenciales obtenidas correctamente.")
    try:
        # Convertir las credenciales en un diccionario y cargar Firebase
        cred_dict = json.loads(cred_data)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except json.JSONDecodeError as e:
        print("Error al procesar el JSON de las credenciales:", e)
        raise ValueError("Las credenciales de Firebase no se pudieron procesar correctamente.")
    except Exception as e:
        print("Error al inicializar Firebase:", e)
        raise ValueError("No se pudo inicializar Firebase con las credenciales proporcionadas.")
else:
    print("No se han encontrado credenciales.")
    raise ValueError("Las credenciales de Firebase no están disponibles en las variables de entorno.")

# Conexión a Firestore
db = firestore.client()

# Función para crear el path del documento
def doc_path(guild_id, weapon_name):
    return f"loadouts/{guild_id}_{weapon_name}"

# Función para guardar un loadout
async def save_loadout(guild_id, weapon_name, data):
    path = doc_path(guild_id, weapon_name)
    db.document(path).set(data)

# Función para obtener los loadouts de un servidor
async def get_loadouts(guild_id):
    loadouts_ref = db.collection("loadouts")
    docs = loadouts_ref.stream()
    result = {}
    for doc in docs:
        if doc.id.startswith(f"{guild_id}_"):
            weapon_name = doc.id.split("_", 1)[1]
            result[weapon_name] = doc.to_dict()
    return result

# Función para eliminar un loadout
async def delete_loadout(guild_id, weapon_name):
    path = doc_path(guild_id, weapon_name)
    db.document(path).delete()

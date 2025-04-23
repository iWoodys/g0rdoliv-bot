import sqlite3
import json
import os

DB_NAME = "loadouts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS loadouts (
            guild_id TEXT,
            weapon_name TEXT,
            data TEXT,
            PRIMARY KEY (guild_id, weapon_name)
        )
    ''')
    conn.commit()
    conn.close()

async def save_loadout(guild_id, weapon_name, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO loadouts (guild_id, weapon_name, data)
        VALUES (?, ?, ?)
    ''', (guild_id, weapon_name, json.dumps(data)))
    conn.commit()
    conn.close()

async def get_loadouts(guild_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT weapon_name, data FROM loadouts WHERE guild_id = ?', (guild_id,))
    rows = c.fetchall()
    conn.close()
    return {weapon: json.loads(data) for weapon, data in rows}

async def delete_loadout(guild_id, weapon_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM loadouts WHERE guild_id = ? AND weapon_name = ?', (guild_id, weapon_name))
    conn.commit()
    conn.close()


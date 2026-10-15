"""Gestor de tareas por consola.

Las tareas se guardan en un archivo llamado tareas.json.
"""

import json
from pathlib import Path

# Nombre del archivo donde se guardan las tareas
ARCHIVO = Path("tareas.json")


def cargar_tareas(archivo):
    """Lee las tareas del archivo. Si no existe todavía, devuelve una lista vacía."""
    if not archivo.exists():
        return []
    with open(archivo, encoding="utf-8") as f:
        return json.load(f)


def guardar_tareas(tareas, archivo):
    """Guarda la lista de tareas en el archivo."""
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

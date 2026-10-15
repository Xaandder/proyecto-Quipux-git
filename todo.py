"""Gestor de tareas por consola.

Las tareas se guardan en un archivo llamado tareas.json.

Uso:
    python todo.py agregar "Aprender Git"
    python todo.py listar
    python todo.py hecha 1
"""

import argparse
import json
import sys
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


def agregar_tarea(tareas, texto):
    """Agrega una tarea nueva a la lista y la devuelve."""
    texto = texto.strip()
    if not texto:
        raise ValueError("La tarea no puede estar vacía")
    # El id nuevo es el mayor id actual + 1 (o 1 si todavía no hay tareas)
    nuevo_id = max((t["id"] for t in tareas), default=0) + 1
    tarea = {"id": nuevo_id, "texto": texto, "hecha": False}
    tareas.append(tarea)
    return tarea


def completar_tarea(tareas, id_tarea):
    """Marca como hecha la tarea con ese id y la devuelve."""
    for tarea in tareas:
        if tarea["id"] == id_tarea:
            tarea["hecha"] = True
            return tarea
    raise LookupError(f"No existe la tarea {id_tarea}")


def formatear_tarea(tarea):
    """Devuelve la tarea como texto, por ejemplo: [ ] 1. Aprender Git"""
    marca = "x" if tarea["hecha"] else " "
    return f"[{marca}] {tarea['id']}. {tarea['texto']}"


def main(argv=None):
    # argparse lee lo que escribes en la consola y lo convierte en datos
    parser = argparse.ArgumentParser(description="Gestor de tareas por consola")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_agregar = sub.add_parser("agregar", help="Agrega una tarea nueva")
    p_agregar.add_argument("texto", help="Texto de la tarea")

    sub.add_parser("listar", help="Muestra todas las tareas")

    p_hecha = sub.add_parser("hecha", help="Marca una tarea como hecha")
    p_hecha.add_argument("id", type=int, help="Número de la tarea")

    args = parser.parse_args(argv)
    tareas = cargar_tareas(ARCHIVO)

    try:
        if args.comando == "agregar":
            tarea = agregar_tarea(tareas, args.texto)
            guardar_tareas(tareas, ARCHIVO)
            print(f"Tarea agregada: {formatear_tarea(tarea)}")
        elif args.comando == "listar":
            if not tareas:
                print("No hay tareas todavía.")
            for tarea in tareas:
                print(formatear_tarea(tarea))
        elif args.comando == "hecha":
            tarea = completar_tarea(tareas, args.id)
            guardar_tareas(tareas, ARCHIVO)
            print(f"Tarea completada: {formatear_tarea(tarea)}")
    except (ValueError, LookupError) as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

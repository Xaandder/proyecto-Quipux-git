"""Pruebas del gestor de tareas.

Se ejecutan con:
    python -m unittest -v
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import todo


class PruebasFunciones(unittest.TestCase):
    def test_agregar_asigna_ids_consecutivos(self):
        tareas = []
        todo.agregar_tarea(tareas, "Primera")
        segunda = todo.agregar_tarea(tareas, "Segunda")
        self.assertEqual(segunda["id"], 2)
        self.assertEqual(len(tareas), 2)

    def test_agregar_texto_vacio_falla(self):
        with self.assertRaises(ValueError):
            todo.agregar_tarea([], "   ")

    def test_completar_marca_como_hecha(self):
        tareas = []
        todo.agregar_tarea(tareas, "Estudiar ramas")
        todo.completar_tarea(tareas, 1)
        self.assertTrue(tareas[0]["hecha"])

    def test_completar_tarea_inexistente_falla(self):
        with self.assertRaises(LookupError):
            todo.completar_tarea([], 99)

    def test_eliminar_quita_la_tarea(self):
        tareas = []
        todo.agregar_tarea(tareas, "Bórrame")
        todo.eliminar_tarea(tareas, 1)
        self.assertEqual(tareas, [])

    def test_id_no_se_repite_despues_de_eliminar(self):
        tareas = []
        todo.agregar_tarea(tareas, "Una")
        todo.agregar_tarea(tareas, "Dos")
        todo.eliminar_tarea(tareas, 1)
        nueva = todo.agregar_tarea(tareas, "Tres")
        self.assertEqual(nueva["id"], 3)


class PruebasArchivo(unittest.TestCase):
    def test_cargar_sin_archivo_devuelve_lista_vacia(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "no_existe.json"
            self.assertEqual(todo.cargar_tareas(archivo), [])

    def test_guardar_y_cargar(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "tareas.json"
            tareas = [{"id": 1, "texto": "Probar ñandú", "hecha": False}]
            todo.guardar_tareas(tareas, archivo)
            self.assertEqual(todo.cargar_tareas(archivo), tareas)


class PruebasConsola(unittest.TestCase):
    def test_flujo_completo_por_consola(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "tareas.json"
            # Cambiamos ARCHIVO solo durante la prueba y ocultamos los print
            with mock.patch.object(todo, "ARCHIVO", archivo), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(todo.main(["agregar", "Aprender Git"]), 0)
                self.assertEqual(todo.main(["hecha", "1"]), 0)
                self.assertEqual(todo.main(["hecha", "42"]), 1)
                self.assertEqual(todo.main(["eliminar", "1"]), 0)
            self.assertEqual(todo.cargar_tareas(archivo), [])


if __name__ == "__main__":
    unittest.main()

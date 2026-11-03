
"""Datos inventados para un laboratorio académico, sin información real."""

from pathlib import Path
from contextlib import closing
import sqlite3

USUARIOS = [
    ('alicia_demo', 'clave_demo_101', 'estudiante'),
    ('bruno_demo', 'clave_demo_202', 'docente'),
    ('carla_demo', 'clave_demo_303', 'laboratorio'),
]


def preparar_db(ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # Abrir y cerrar correctamente la conexión SQLite.
    with closing(sqlite3.connect(ruta)) as db:

        db.execute('DROP TABLE IF EXISTS usuarios')

        db.execute(
            'CREATE TABLE usuarios ('
            'id INTEGER PRIMARY KEY, '
            'usuario TEXT NOT NULL UNIQUE, '
            'clave TEXT NOT NULL, '
            'rol TEXT NOT NULL)'
        )

        db.executemany(
            'INSERT INTO usuarios (usuario, clave, rol) '
            'VALUES (?, ?, ?)',
            USUARIOS
        )

        # Guardar los cambios antes de cerrar.
        db.commit()

    return ruta

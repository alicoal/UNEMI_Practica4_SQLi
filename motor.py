
"""Comparación controlada entre SQL inseguro y SQL parametrizado."""

import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, render_template, request
from datos import preparar_db


def crear_app(segura=False, ruta_db=None):
    app = Flask(__name__)
    app.config['SEGURA'] = bool(segura)

    if ruta_db is None:
        ruta_db = (
            Path(__file__).resolve().parent
            / 'datos_locales'
            / ('segura.sqlite3' if segura else 'vulnerable.sqlite3')
        )

    app.config['RUTA_DB'] = str(ruta_db)

    if not Path(ruta_db).exists():
        preparar_db(ruta_db)

    @app.route('/', methods=['GET'])
    def inicio():
        return render_template('inicio.html', segura=segura)

    @app.route('/login', methods=['POST'])
    def login():
        usuario = request.form.get('usuario', '')
        clave = request.form.get('clave', '')

        if len(usuario) > 150 or len(clave) > 150:
            return {
                'autenticado': False,
                'mensaje': 'Entrada demasiado larga'
            }, 400

        # closing garantiza el cierre de la conexión SQLite.
        with closing(sqlite3.connect(app.config['RUTA_DB'])) as db:
            db.row_factory = sqlite3.Row

            if segura:
                # VERSION PROTEGIDA: consulta parametrizada.
                fila = db.execute(
                    'SELECT id, usuario, rol FROM usuarios '
                    'WHERE usuario = ? AND clave = ?',
                    (usuario, clave)
                ).fetchone()

            else:
                # VERSION VULNERABLE: solamente para el laboratorio
                # local con datos ficticios. Nunca usar en produccion.
                sql = (
                    "SELECT id, usuario, rol FROM usuarios "
                    "WHERE usuario = '" + usuario +
                    "' AND clave = '" + clave + "'"
                )

                try:
                    fila = db.execute(sql).fetchone()
                except sqlite3.Error:
                    return {
                        'autenticado': False,
                        'mensaje': 'Consulta rechazada'
                    }, 400

        return {
            'autenticado': fila is not None,
            'usuario': dict(fila)['usuario'] if fila else None,
            'modo': 'protegido' if segura else 'vulnerable'
        }

    @app.route('/buscar', methods=['GET'])
    def buscar():
        termino = request.args.get('q', '')

        if len(termino) > 150:
            return {
                'mensaje': 'Entrada demasiado larga'
            }, 400

        # La conexión se cierra al salir del bloque.
        with closing(sqlite3.connect(app.config['RUTA_DB'])) as db:
            db.row_factory = sqlite3.Row

            if segura:
                # VERSION PROTEGIDA: consulta parametrizada.
                filas = db.execute(
                    'SELECT id, usuario, rol FROM usuarios '
                    'WHERE usuario LIKE ?',
                    ('%' + termino + '%',)
                ).fetchall()

            else:
                # VERSION VULNERABLE: concatenación insegura
                # únicamente para la demostración académica.
                sql = (
                    "SELECT id, usuario, rol FROM usuarios "
                    "WHERE usuario LIKE '%" + termino + "%'"
                )

                try:
                    filas = db.execute(sql).fetchall()
                except sqlite3.Error:
                    return {
                        'mensaje': 'Consulta rechazada'
                    }, 400

        return {
            'total': len(filas),
            'registros': [dict(f) for f in filas],
            'modo': 'protegido' if segura else 'vulnerable'
        }

    return app

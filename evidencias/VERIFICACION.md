# Verificación técnica — 3 de noviembre de 2026

Ejecución real sobre la copia preparada; no constituye el informe académico final ni una contribución atribuida a integrantes.

- Windows, Python 3.12.6; dependencias en `requirements-lock.txt`.
- `python -m pytest -v`: **5 passed in 0.61s**. Salida en `pytest.txt`; se omitieron las rutas personales.
- `ataque_sql_i.ejecutar(5000)` y `ejecutar(5001)`: cinco escenarios por versión contra servidores HTTP Werkzeug en 127.0.0.1, con bases temporales. Respuestas auténticas en `ataque_5000.jsonl` y `ataque_5001.jsonl`.
- Login válido: verdadero en ambas; inválido: falso en ambas; SQLi: verdadero solo en vulnerable. Búsqueda ordinaria: un registro en ambas; SQLi: tres en vulnerable y cero en parametrizada. Todas las respuestas HTTP fueron 200.
- Ambas plantillas devolvieron 200 mediante el cliente de prueba Flask. No se realizó inspección visual en navegador ni se generaron capturas.
- `escaneo_red.py`: conexión TCP aceptada al puerto de cada servidor durante su ejecución. Véanse las salidas correspondientes.
- Servidores detenidos y bases temporales eliminadas al terminar.

## Revisión de código
`motor.py` y `datos.py` conservan `contextlib.closing`; las lecturas finalizan antes de cerrar y la inicialización confirma los cambios con `commit`. No se modificaron estas correcciones.

`ataque_sql_i.py` mantiene destino fijo 127.0.0.1 y puertos 5000/5001. Se deshabilitaron proxies y redirecciones HTTP. La versión parametrizada protege las consultas estudiadas; el login sigue siendo didáctico, con contraseñas ficticias en texto claro y sin sesiones.

## Pendientes externos
La guía oficial y rúbrica no se adjuntaron: los requisitos mencionados en la conversación anterior no se consideran verificados contra el documento. No se verificaron contribuciones grupales. Publicación, permisos e invitaciones requieren autorización del propietario. No se creó remoto ni se publicó o desplegó contenido.

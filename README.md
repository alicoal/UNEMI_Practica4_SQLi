# UNEMI - Práctica 4: SQL Injection

Laboratorio didáctico local con Flask + SQLite, preparado para la asignatura Seguridad Informática.

**ADVERTENCIA:** `app_vulnerable.py` contiene SQL inseguro a propósito. No exponer a Internet o a la LAN, no cargar datos reales, no reutilizar para producción. Los servidores escuchan solamente en `127.0.0.1`.

## Archivos requeridos
- `app_vulnerable.py`: aplicación con SQL concatenado intencionadamente.
- `ataque_sql_i.py`: pruebas automatizadas para los puertos LOCALES 5000 y 5001.
- `escaneo_red.py`: escáner TCP limitado a loopback.
- `README.md`: descripción del proyecto.
- `MANUAL_USO.md`: guía detallada.

## Archivos complementarios
- `app_segura.py`: versión corregida con consultas parametrizadas.
- `motor.py`: aplicación compartida para comparación de ambas estrategias.
- `datos.py`: creación de usuarios ficticios en SQLite.
- `templates/inicio.html`: interfaz visual.
- `tests/test_laboratorio.py`: pruebas `unittest` reproducibles.
- `requirements.txt`: versión de Flask verificada.
- `requirements-dev.txt`: dependencias para pytest.

## Inicio rápido (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app_vulnerable.py
```
Abra http://127.0.0.1:5000/ y consulte `MANUAL_USO.md` para ejecutar los dos servidores y las pruebas.

## Alcance
La autenticación es una simplificación para demostrar SQL Injection, **no un sistema de login seguro para producción**: las contraseñas de prueba se almacenan en texto claro y no se crean sesiones reales. La corrección estudiada es la parametrización SQL, no una auditoría integral de autenticación.

## Evidencias académicas
Los resultados y capturas deben obtenerse realmente desde las computadoras de los integrantes. No publicar contraseñas, secretos ni capturas con información personal. La contribución de cada integrante deberá ser verificable.

## Verificación reproducible
Desde la carpeta del proyecto, sin activar el entorno virtual:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pytest -v
```
Resultado esperado: cinco pruebas aprobadas. No requieren servidores activos y utilizan bases temporales. Consulte `evidencias/VERIFICACION.md` para la ejecución real de esta revisión.

`requirements-lock.txt` fija las dependencias del entorno verificado en Windows con Python 3.12.6; otras plataformas o versiones deben validarse por separado. Alternativamente, instale `requirements-dev.txt` para resolver las dependencias transitivas compatibles.

## Ejecución local

El código está disponible en GitHub para su descarga y ejecución local. Las aplicaciones utilizan datos ficticios y escuchan exclusivamente en `127.0.0.1`, en los puertos 5000 y 5001. Las bases de datos se crean al iniciar las aplicaciones y el entorno virtual se prepara durante la instalación; ninguno forma parte del repositorio.
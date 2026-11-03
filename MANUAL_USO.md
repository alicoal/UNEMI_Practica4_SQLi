# Manual de uso y pruebas — Práctica N.º 4

## 1. Requisitos
- Windows 10/11, macOS o Linux; Python 3.10+; conexión a Internet durante instalación de Flask.
- Visual Studio Code opcional; Git y cuenta GitHub para el repositorio grupal.

## 2. Instalar en Windows (PowerShell)
Abra la carpeta del proyecto en VS Code, luego Terminal > Nueva terminal.
```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
```
Si su equipo no reconoce `py`, utilice `python`. En Linux/macOS use `python3 -m venv .venv`, `source .venv/bin/activate` y `python -m pip install -r requirements-lock.txt`.

## 3. Arrancar las dos versiones
Abra dos terminales en la carpeta, con el entorno virtual activo.
Terminal 1:
```powershell
python app_vulnerable.py
```
Terminal 2:
```powershell
python app_segura.py
```
Abra estas direcciones SOLO en su propio equipo:
- Vulnerable: http://127.0.0.1:5000/
- Protegida: http://127.0.0.1:5001/

Al iniciar se crean bases de datos separadas en `datos_locales/`, con tres usuarios ficticios.

## 4. Pruebas manuales
- Ingrese `alicia_demo` y `clave_demo_101` en el formulario: en ambos modos debería autenticarse.
- Ingrese `alicia_demo` y `incorrecta`: en ambos debería rechazarse.
- Para demostrar bypass de autenticación en su servidor local, ingrese como usuario: `' OR '1'='1' -- `; como clave: `incorrecta`. Compare las respuestas de los dos modos.
- En búsqueda, ingrese `alicia`: debería mostrarse un registro en ambos modos.
- En búsqueda, ingrese `' OR '1'='1' -- `: compare la cantidad de registros obtenidos en cada modo.

Nota: estos valores de demostración solo están autorizados en esta aplicación creada para la práctica.

## 5. Pruebas automatizadas
Abra una tercera terminal:
```powershell
python ataque_sql_i.py --puerto 5000
python ataque_sql_i.py --puerto 5001
python -m pytest -v
# Alternativa sin pytest:
python -m unittest discover -s tests -v
```
El script de ataque no permite objetivos de red arbitrarios: utiliza exclusivamente loopback y los puertos del laboratorio.

## 6. Escaneo de puertos del propio equipo
Con ambos servidores activos:
```powershell
python escaneo_red.py --puertos 5000 5001
```
Una conexión aceptada demuestra que hay un servicio TCP escuchando en esa dirección y puerto, no identifica automáticamente su producto.

## 7. Qué documentar en el informe
Registre por cada prueba: fecha, nombre del integrante, escenario, versión, entrada, estado HTTP, resultado esperado, respuesta real y captura. Incluya capturas de:
1. Terminales ejecutando los servidores locales.
2. Formulario de login de ambas versiones.
3. Pruebas de bypass, búsqueda y mitigación.
4. Pruebas `unittest` y escaneo local.
5. Archivos del repositorio y participación verificable del grupo.

No fabrique ni altere resultados de pruebas. Si una prueba falla, registre la falla y su causa.

## 8. Endurecimiento complementario de SQLite
- Evitar SQL concatenado: usar consultas con parámetros.
- Mantener el archivo `.sqlite3` fuera de un directorio web público.
- Restringir permisos de lectura/escritura al usuario del sistema que ejecuta Flask.
- No publicar datos reales ni secretos en GitHub; mantener los `.sqlite3` fuera del repositorio.
- Aplicar integridad referencial cuando haya relaciones (`PRAGMA foreign_keys=ON`).
- Conservar una copia recuperable de datos de laboratorio si se realizan pruebas destructivas (este proyecto no realiza ninguna).
- No revelar detalles de excepciones SQL al visitante de la aplicación.

## 9. Repositorio GitHub
Esta copia se prepara localmente. Antes de publicar, revisar `git status --short`, `git diff --cached` y `git ls-files`; no deben incluir bases, secretos, entornos ni datos personales. La publicación, los cambios de permisos y las invitaciones requieren autorización expresa del propietario. No se ha configurado un remoto ni se ha enviado contenido a GitHub.

Después de obtener autorización se podrá crear el repositorio, configurar su URL y publicar. El profesor podrá descargar o clonar el código y seguir los pasos anteriores en su propio equipo. No necesita un sitio público ejecutando Flask. Registrar únicamente contribuciones auténticas; esta copia no asigna autoría grupal ni una licencia sin acuerdo.

Para reiniciar los datos ficticios, detener ambos servidores y eliminar únicamente los archivos `datos_locales/vulnerable.sqlite3` y `datos_locales/segura.sqlite3` de esta copia. Se regeneran al iniciar. No usar `flask run --host=0.0.0.0`, túneles ni alojamiento público.

## 10. Advertencia de alcance
Este laboratorio es intencionalmente vulnerable y deliberadamente limitado. No representa un login de producción ni demuestra seguridad integral. La prueba de mitigación evalúa exclusivamente que los parámetros del usuario no modifiquen la estructura SQL.

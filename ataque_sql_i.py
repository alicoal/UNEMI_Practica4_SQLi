"""Pruebas reproducibles SOLO contra el servidor local del proyecto."""
import argparse
import json
from urllib.parse import urlencode
from urllib.request import Request, build_opener, ProxyHandler, HTTPRedirectHandler

INYECCION = "' OR '1'='1' -- "


class SinRedirecciones(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def solicitud(url, datos=None):
    contenido = urlencode(datos).encode() if datos is not None else None
    peticion = Request(url, data=contenido, method='POST' if datos is not None else 'GET')
    # Ignorar proxies del sistema y rechazar redirecciones fuera del laboratorio.
    opener = build_opener(ProxyHandler({}), SinRedirecciones())
    with opener.open(peticion, timeout=4) as respuesta:
        return respuesta.status, json.loads(respuesta.read().decode('utf-8'))


def ejecutar(puerto):
    if puerto not in (5000, 5001):
        raise ValueError('Solo se permiten los puertos locales 5000 y 5001.')
    base = f'http://127.0.0.1:{puerto}'
    escenarios = [
        ('Login válido', '/login', {'usuario': 'alicia_demo', 'clave': 'clave_demo_101'}),
        ('Login inválido', '/login', {'usuario': 'alicia_demo', 'clave': 'incorrecta'}),
        ('Login con SQLi de demostración', '/login', {'usuario': INYECCION, 'clave': 'incorrecta'}),
        ('Búsqueda ordinaria', '/buscar?' + urlencode({'q': 'alicia'}), None),
        ('Búsqueda con SQLi de demostración', '/buscar?' + urlencode({'q': INYECCION}), None),
    ]
    for nombre, ruta, datos in escenarios:
        estado, contenido = solicitud(base + ruta, datos)
        print(json.dumps({'escenario': nombre, 'http': estado, 'respuesta': contenido}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pruebas SQLi confinadas a 127.0.0.1')
    parser.add_argument('--puerto', type=int, choices=[5000, 5001], required=True)
    args = parser.parse_args()
    try:
        ejecutar(args.puerto)
    except OSError as exc:
        raise SystemExit(f'No se pudo conectar al laboratorio local: {exc}')

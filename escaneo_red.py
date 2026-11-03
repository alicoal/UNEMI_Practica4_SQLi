"""Escaneo TCP básico RESTRINGIDO a loopback."""
import argparse
import socket

def escanear(puertos):
    for puerto in puertos:
        if not 1 <= puerto <= 65535:
            raise ValueError('Puerto fuera del rango TCP')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            codigo = sock.connect_ex(('127.0.0.1', puerto))
        print(f'127.0.0.1:{puerto} -> {"conexión TCP aceptada" if codigo == 0 else "sin conexión TCP"}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Revisa solo puertos locales')
    parser.add_argument('--puertos', type=int, nargs='+', default=[5000, 5001])
    args = parser.parse_args()
    if len(args.puertos) > 10:
        parser.error('Máximo 10 puertos por ejecución')
    escanear(args.puertos)

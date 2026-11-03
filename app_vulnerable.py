"""SOLO LOCAL: aplicación deliberadamente vulnerable para la guía UNEMI."""
from motor import crear_app
app = crear_app(segura=False)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

"""Pruebas de laboratorio con bases de datos temporales."""
import tempfile
import unittest
from pathlib import Path
from motor import crear_app
from datos import preparar_db

INYECCION = "' OR '1'='1' -- "

class PruebaLaboratorio(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        carpeta = Path(self.temp.name)
        self.db_vul = preparar_db(carpeta / 'vulnerable.sqlite3')
        self.db_seg = preparar_db(carpeta / 'segura.sqlite3')
        self.vulnerable = crear_app(False, self.db_vul).test_client()
        self.segura = crear_app(True, self.db_seg).test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_login_legitimo_funciona_en_ambas(self):
        for cliente in (self.vulnerable, self.segura):
            r = cliente.post('/login', data={'usuario':'alicia_demo','clave':'clave_demo_101'})
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.json['autenticado'])

    def test_login_falso_falla_en_ambas(self):
        for cliente in (self.vulnerable, self.segura):
            r = cliente.post('/login', data={'usuario':'alicia_demo','clave':'incorrecta'})
            self.assertFalse(r.json['autenticado'])

    def test_inyeccion_solo_engana_a_vulnerable(self):
        datos={'usuario':INYECCION,'clave':'incorrecta'}
        self.assertTrue(self.vulnerable.post('/login',data=datos).json['autenticado'])
        self.assertFalse(self.segura.post('/login',data=datos).json['autenticado'])

    def test_busqueda_inyeccion_expone_solo_en_vulnerable(self):
        self.assertEqual(self.vulnerable.get('/buscar',query_string={'q':INYECCION}).json['total'],3)
        self.assertEqual(self.segura.get('/buscar',query_string={'q':INYECCION}).json['total'],0)

    def test_busqueda_ordinaria_funciona_en_ambas(self):
        for cliente in (self.vulnerable,self.segura):
            self.assertEqual(cliente.get('/buscar',query_string={'q':'alicia'}).json['total'],1)

if __name__ == '__main__':
    unittest.main()

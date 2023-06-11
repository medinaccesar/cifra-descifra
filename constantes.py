import os


class Configuracion:

    __slots__ = ()

    NOMBRE_AP = 'Cifradescifra'
    DESCRIPCION_APP = 'Cifra y descifra archivos'
    VERSION = '1.1.0'
    CREDITOS = 'César Medina'

    # Clave maestra para un cifrado de doble capa, sustituir la clave maestra y el salt
    CLAVE_MAESTRA = b'mi_propia_clave'
    SALT = b'mi_propio_salto'

    # Directorios
    DIR_DOCUMENTOS = os.path.expanduser("~")
    DIR_ABS = os.path.dirname(os.path.abspath(__file__))+os.path.sep
    DIR_BD = 'data'+os.path.sep
    DIR_DB_BACKUP = DIR_BD+os.path.sep+'backup'+os.path.sep
    DIR_IMA = 'rec'+os.path.sep+'ima'+os.path.sep

    # Extensión archivo cifrado
    EXT_ARCHIVO_CIFRADO = '.cifrado'

    # En función del tamaño del archivo se elige el método para calcular el hash, o bien se lee en memoria entero o se divide en partes
    TAMANNO_MAX_ARCHIVO_CALC_HASH = 524280000  # 500M

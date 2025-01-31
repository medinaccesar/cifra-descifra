import os


class Configuracion:

    __slots__ = ()

    NOMBRE_AP = 'Cifradescifra'
    DESCRIPCION_APP = 'Cifra y descifra archivos'
    VERSION = '2.0.0'
    CREDITOS = 'César Medina'

    # Clave maestra para un cifrado de doble capa, sustituir la clave maestra y el salt
    CLAVE_MAESTRA = b'mi_propia_clave'
    SALT = b'mi_propio_sal'

    # Directorios
    DIR_DOCUMENTOS = os.path.expanduser("~")
    DIR_ABS = os.path.dirname(os.path.abspath(__file__))+os.path.sep
    DIR_BD = 'data'+os.path.sep
    NOMBRE_BD = 'database.db'
    DIR_DB_BACKUP = DIR_BD+os.path.sep+'backup'+os.path.sep
    DIR_IMA = 'rec'+os.path.sep+'ima'+os.path.sep
    
    

    # Extensión archivo cifrado
    EXT_ARCHIVO_CIFRADO = '.cifrado'
    
    # Nombre de los archivos de la clave pública y privada del usuario que pueden ser exportados para otros fines.
    NOMBRE_ARCHIVO_CLAVE_PUBLICA = 'clave.pub'
    NOMBRE_ARCHIVO_CLAVE_PRIVADA = 'clave.pem'
    # Extensión del archivo donde se exporta la clave de cifrado, del archivo cifrado, cifrada 
    #  con la clave pública de cada uno de los usuarios con los que se comparte.
    EXT_ARCHIVO_LLAVE = '.llave' 
    
    # Tipos de cifrado
    CIFRADO_AES128_CBC = 'AES128_CBC'
    CIFRADO_AES256_GCM = 'AES256_GCM'
    CIFRADO_CHACHA20_POLY1305 = 'XChaCha20_POLY1305'
    # (...)
    
    # Cifrado por defecto de la aplicación
    TIPO_CIFRADO_DEFECTO = CIFRADO_AES256_GCM

    # En función del tamaño del archivo se elige el método para calcular el hash, o bien se lee en memoria entero o se divide en partes
    TAMANNO_MAX_ARCHIVO_CALC_HASH = 524280000  # 500M

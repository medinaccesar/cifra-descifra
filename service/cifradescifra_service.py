import hashlib
import os
import re
from service.cifrado_doble_service import CifradoDobleCapa
from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from constantes import Configuracion as conf
from cryptography.fernet import Fernet
from datetime import datetime

class CifraDescifraArchivo():

    def __init__(self):
        self._cifrado_doble_capa = CifradoDobleCapa()

    # Calcula el hash del archivo
    def calcular_hash_archivo(self, ruta_archivo):
        
        tamanno = os.path.getsize(ruta_archivo)
        
        if tamanno < conf.TAMANNO_MAX_ARCHIVO_CALC_HASH:
            return self._calcular_hash_archivo_normal(ruta_archivo)

        return self._calcular_hash_archivo_grande(ruta_archivo)
    
    # Calcula el hash cargando el archivo entero en memoria
    def _calcular_hash_archivo_normal(self, ruta_archivo):
        
        hash_archivo = None
        
        with open(ruta_archivo, 'rb') as f:
            data = f.read()
            hash_archivo = hashlib.sha256(data).hexdigest()

        return hash_archivo
   
    # Calcula el hash cargando el archivo por partes
    def _calcular_hash_archivo_grande(self, ruta_archivo):
        
        BUF_SIZE = 1024
        hasher = hashlib.new('sha256')

        with open(ruta_archivo, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                hasher.update(data)

        return hasher.hexdigest()
    
    def calcular_hash_cadena(self, nombre_archivo):
        hash_nombre_archivo = hashlib.sha256(nombre_archivo.encode()).hexdigest()
        return hash_nombre_archivo

    def cifrar_archivo(self, ruta_archivo, ruta_archivo_cifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido = self.leer_archivo(ruta_archivo)
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico
        # Se genera una clave secreta
        clave = Fernet.generate_key()
        # Se crea un objeto Fernet con la clave secreta
        fernet = Fernet(clave)
        # Se cifra el contenido del archivo
        contenido_cifrado = fernet.encrypt(contenido)
        if callback: callback(40)
        clave_cifrada = self._cifrado_doble_capa.cifrar_clave(clave)        
        self.escribir_archivo(ruta_archivo_cifrado, contenido_cifrado)
        if callback: callback(25)        
        hash_archivo = self.calcular_hash_archivo(ruta_archivo_cifrado)       
        conexion_bd.insertar_registro(hash_archivo, clave_cifrada)
        if callback: callback(5)

    def descifrar_archivo(self, ruta_archivo_cifrado, nombre_archivo_descifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido_cifrado = self.leer_archivo(ruta_archivo_cifrado)
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico 
        hash_archivo = self.calcular_hash_archivo(ruta_archivo_cifrado)        
        clave_cifrada = conexion_bd.obtener_clave_cifrada(hash_archivo)
        if callback: callback(20)
        # TODO: gestionar si no hay clave
        clave = self._cifrado_doble_capa.descifrar_clave(clave_cifrada)
        fernet = Fernet(clave)
        if callback: callback(25)       
        # Se descifra el contenido del archivo
        contenido_descifrado = fernet.decrypt(contenido_cifrado)
        if callback: callback(20)        
        self.escribir_archivo(nombre_archivo_descifrado, contenido_descifrado)
        if callback: callback(10)

    def leer_archivo(self, ruta_archivo):
        with open(ruta_archivo, 'rb') as archivo:
            contenido = archivo.read()
        return contenido

    def escribir_archivo(self, ruta_archivo, contenido):
        with open(ruta_archivo, 'wb') as archivo:
            archivo.write(contenido)

    def marca_temporal(self):
        ahora = datetime.now()
        return ahora.strftime('%y%m%d_%H%M%S')

    def quitar_ext_cifrado(self, nombre_archivo):
        partes = nombre_archivo.split(".")
        return ".".join(partes[:-1])

    def quitar_marca_temporal(self, nombre_archivo):        
        sufijo = nombre_archivo[-14:] if len(nombre_archivo) > 14 else ''
        match = re.match(r"\_\d{6}_\d{6}$", sufijo)
        if match:           
            return nombre_archivo[:-14]
        else:          
            return nombre_archivo

    def obtener_nombre_original(self, nombre_archivo):
        nombre_archivo = self.quitar_ext_cifrado(nombre_archivo)
        nombre_archivo = self.quitar_marca_temporal(nombre_archivo)
        return nombre_archivo

    def annadir_marca_temporal(self, nombre_archivo):
        marca_temporal = self.marca_temporal()
        # Se extrae la extensión del archivo
        extension = os.path.splitext(nombre_archivo)[1]
        # Se concatena la extensión con la marca temporal
        nombre_archivo = nombre_archivo[:-
                                        len(extension)] +'_'+ marca_temporal + extension
        return nombre_archivo

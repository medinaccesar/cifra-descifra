
import os
from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from constantes import Configuracion as conf
from service.cifradescifra_service import CifraDescifraArchivo
from chacha20poly1305 import ChaCha20Poly1305

class CifraDescifraArchivoXChachaPoly(CifraDescifraArchivo):

    def __init__(self):
        super().__init__()
        self._tipocifrado = conf.CIFRADO_CHACHA20_POLY1305

    def cifrar_archivo(self, ruta_archivo, ruta_archivo_cifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido = self._fichero.leer_archivo(ruta_archivo)
        if contenido is None:
            return False
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico
        # Se genera una clave secreta y un número de un solo uso   
        clave = self.getClave()
        nonce = os.urandom(12) 
        cipher = ChaCha20Poly1305(clave)                 
        # Se cifra el contenido del archivo
        contenido_cifrado =  cipher.encrypt(nonce, contenido)
        if callback: callback(40)
        contenido_cifrado =  nonce + contenido_cifrado        
        clave_cifrada = self._cifrado_doble_capa.cifrar_clave(clave)      
             
        self._fichero.escribir_archivo(ruta_archivo_cifrado, contenido_cifrado)
        if callback: callback(25)        
        hash_archivo = self._hash_service.calcular_hash_archivo(ruta_archivo_cifrado)       
        conexion_bd.insertar_registro(hash_archivo, clave_cifrada,'1', self._tipocifrado)
        if callback: callback(5)
        return True

    def descifrar_archivo(self, ruta_archivo_cifrado, nombre_archivo_descifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido_cifrado = self._fichero.leer_archivo(ruta_archivo_cifrado)
        if contenido_cifrado is None:
            return False
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico 
        hash_archivo = self._hash_service.calcular_hash_archivo(ruta_archivo_cifrado)        
        clave_cifrada = conexion_bd.obtener_clave_cifrada(hash_archivo)
        if callback: callback(20)
        # TODO: gestionar si no hay clave
        clave = self._cifrado_doble_capa.descifrar_clave(clave_cifrada)       
        cipher = ChaCha20Poly1305(clave)
        if callback: callback(25)       
        # Se descifra el contenido del archivo        
        nonce = contenido_cifrado[:12]
        texto_cifrado = contenido_cifrado[12:]
        contenido_descifrado = cipher.decrypt(nonce, texto_cifrado)       
        if callback: callback(20)        
        self._fichero.escribir_archivo(nombre_archivo_descifrado, contenido_descifrado)
        if callback: callback(5)
        return True
    
    def getClave(self):
        return os.urandom(32)

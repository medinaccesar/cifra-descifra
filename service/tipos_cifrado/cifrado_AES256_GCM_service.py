
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from constantes import Configuracion as conf
from service.cifradescifra_service import CifraDescifraArchivo


class CifraDescifraArchivoAES256GCM(CifraDescifraArchivo):

    def __init__(self):
        super().__init__()
        self._tipocifrado = conf.CIFRADO_AES256_GCM

    def cifrar_archivo(self, ruta_archivo, ruta_archivo_cifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido = self._fichero.leer_archivo(ruta_archivo)
        if contenido is None:
            return False
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico
        # Se genera una clave secreta y un vector de inicialización
        clave = os.urandom(32)       
        iv = os.urandom(16) # mejor 12 ¿?
        # Se crea un objeto con la clave secreta
        cipher = Cipher(algorithms.AES(clave), modes.GCM(iv), backend=default_backend())
        
        encryptor = cipher.encryptor()        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(contenido) + padder.finalize()
        contenido_cifrado = encryptor.update(padded_data) + encryptor.finalize()
        if callback: callback(40)
        tag = encryptor.tag
        clave_cifrada = self._cifrado_doble_capa.cifrar_clave(clave)        
        iv_cifrado = self._cifrado_doble_capa.cifrar_clave(iv+tag)        
        self._fichero.escribir_archivo(ruta_archivo_cifrado, contenido_cifrado)
        if callback: callback(25)        
        hash_archivo = self._hash_service.calcular_hash_archivo(ruta_archivo_cifrado)       
        conexion_bd.insertar_registro(hash_archivo, clave_cifrada, iv_cifrado, self._tipocifrado)
        if callback: callback(5)
        return True
    def descifrar_archivo(self, ruta_archivo_cifrado, nombre_archivo_descifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido_cifrado = self._fichero.leer_archivo(ruta_archivo_cifrado)
        if contenido_cifrado is None:
            return False
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico 
        hash_archivo = self._hash_service.calcular_hash_archivo(ruta_archivo_cifrado)        
        clave_cifrada, adicional_cifrado = conexion_bd.obtener_clave_cifrada_adicional_cifrado(hash_archivo)
        if callback: callback(20)
        # TODO: gestionar si no hay clave
        clave = self._cifrado_doble_capa.descifrar_clave(clave_cifrada)
        adicional = self._cifrado_doble_capa.descifrar_clave(adicional_cifrado)
        tag = adicional[-16:]  
        vi = adicional[:16]
        cipher = Cipher(algorithms.AES(clave), modes.GCM(vi,tag), backend=default_backend())
        if callback: callback(25)       
        # Se descifra el contenido del archivo
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = decryptor.update(contenido_cifrado) + decryptor.finalize()
        contenido_descifrado = unpadder.update(decrypted_data) + unpadder.finalize()
        if callback: callback(20)        
        self._fichero.escribir_archivo(nombre_archivo_descifrado, contenido_descifrado)
        if callback: callback(5)
        return True

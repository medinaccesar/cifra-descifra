
from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from cryptography.fernet import Fernet
from service.cifradescifra_service import CifraDescifraArchivo
from constantes import Configuracion as conf

class CifraDescifraArchivoAES128CBC(CifraDescifraArchivo):

    def __init__(self):
        super().__init__()
        self._tipocifrado = conf.CIFRADO_AES128_CBC
    
        
    def cifrar_archivo(self, ruta_archivo, ruta_archivo_cifrado, callback = None):
        conexion_bd = ConexionBdSqlite()
        contenido = self._fichero.leer_archivo(ruta_archivo)
        if contenido is None:
            return False
        if callback:callback(20) # Avance de la barra de progreso en el entorno gráfico
        # Se genera una clave secreta
        clave = Fernet.generate_key()
        # Se crea un objeto Fernet con la clave secreta
        fernet = Fernet(clave)
        # Se cifra el contenido del archivo
        contenido_cifrado = fernet.encrypt(contenido)
        if callback: callback(40)
        clave_cifrada = self._cifrado_doble_capa.cifrar_clave(clave)        
        self._fichero.escribir_archivo(ruta_archivo_cifrado, contenido_cifrado)
        if callback: callback(25)        
        hash_archivo = self._hash_service.calcular_hash_archivo(ruta_archivo_cifrado)       
        conexion_bd.insertar_registro(hash_archivo, clave_cifrada,'0', self.getTipoCifrado())
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
        fernet = Fernet(clave)
        if callback: callback(25)       
        # Se descifra el contenido del archivo
        contenido_descifrado = fernet.decrypt(contenido_cifrado)
        if callback: callback(20)        
        self._fichero.escribir_archivo(nombre_archivo_descifrado, contenido_descifrado)
        if callback: callback(5)    
        return True

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from constantes import Configuracion as conf
from service.fichero_service import Fichero
# pip install rsa
class CifradoAsimetrico():
    
    def __init__(self):
        self._fichero = Fichero()
    
    def generar_claves(self):
        key = RSA.generate(2048)  # Genera una clave de 2048 bits
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
   
    def generar_claves_cifrafa(self):
        key = RSA.generate(2048)  # Genera una clave de 2048 bits       
        private_key = key.export_key(passphrase=conf.CLAVE_MAESTRA)
        public_key = key.publickey().export_key()
        return private_key, public_key
    
    def cifrar(self, message, public_key):
        public_key = RSA.import_key(public_key) 
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message
    
    def descifrar(self,encrypted_message, private_key):
        private_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message).decode()
        return decrypted_message
    
    # Guarda la clave que se le pasa en un fichero
    def guardar_clave_privada_fichero(self, clave, path = None):
       return self._guardar_clave_fichero(clave, conf.NOMBRE_ARCHIVO_CLAVE_PRIVADA, path )
   
    def guardar_clave_publica_fichero(self, clave, path = None):
        return self._guardar_clave_fichero(clave, conf.NOMBRE_ARCHIVO_CLAVE_PUBLICA, path )
   
    def _guardar_clave_fichero(self, clave, nombre,  path = None):
        if path is None:
            path = conf.DIR_DOCUMENTOS + nombre 
        self._fichero.escribir_archivo(path, clave)
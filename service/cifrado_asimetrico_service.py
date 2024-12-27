from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from constantes import Configuracion as conf
from service.fichero_service import Fichero

class CifradoAsimetrico():
    
    def __init__(self):
        self._fichero = Fichero()
    
    def generar_claves(self):
        key = RSA.generate(2048)  # Genera una clave de 2048 bits
        private_key = key.export_key()  # Se genera transparente
        public_key = key.publickey().export_key()
        return private_key, public_key
   
    def generar_claves_cifrada(self):
        key = RSA.generate(2048)  # Genera una clave de 2048 bits       
        private_key = key.export_key(passphrase=conf.CLAVE_MAESTRA)  # Se genera cifrada
        
        public_key = key.publickey().export_key()
        return private_key, public_key
    
    def recuperar_clave_privada_transparente(self,private_key):
        clave_privada_transparente = RSA.import_key(private_key, passphrase=conf.CLAVE_MAESTRA)
        return clave_privada_transparente
    
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
    
    # Exporta la clave que se le pasa en un fichero
    def exportar_clave_privada_fichero(self, clave, path = None):
       return self._guardar_clave_fichero(clave, conf.NOMBRE_ARCHIVO_CLAVE_PRIVADA, path )
   
    def exportar_clave_publica_fichero(self, clave, correo, path=None):
        data = {
            "clave_publica": clave.decode() if isinstance(clave, bytes) else clave,
            "correo_electronico": correo
        }
        return self._fichero._guardar_clave_fichero(data, conf.NOMBRE_ARCHIVO_CLAVE_PUBLICA, path )
   
    def importar_clave_publica_fichero(self, ruta_archivo):
        return self._fichero.importar_clave_publica_fichero(ruta_archivo)
        
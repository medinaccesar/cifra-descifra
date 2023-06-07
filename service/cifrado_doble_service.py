import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from constantes import Configuracion as conf

class CifradoDobleCapa():
    
    def __init__(self):
         
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=conf.SALT,
            iterations=100000,
            backend=default_backend()
        )        
        self._clave_maestra=  base64.urlsafe_b64encode(kdf.derive(conf.CLAVE_MAESTRA))  
      
        
    def cifrar_clave(self,clave):        
        fernet_maestra = Fernet(self._clave_maestra)        
        clave_cifrada = fernet_maestra.encrypt(clave) 
        return clave_cifrada.decode()
    
    def descifrar_clave(self,clave_cifrada):
        fernet_maestra = Fernet(self._clave_maestra)       
        clave = fernet_maestra.decrypt(clave_cifrada.encode()) 
        return clave


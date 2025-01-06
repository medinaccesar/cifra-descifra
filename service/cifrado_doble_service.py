import base64
import os
import random
import string
from constantes import Configuracion as conf
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class CifradoDobleCapa:
    
    def __init__(self):
              
        salt = conf.SALT
        kdf = self._get_kdf(salt)     
        clave_derivada = kdf.derive(conf.CLAVE_MAESTRA)  
        self._clave_maestra =  base64.urlsafe_b64encode(clave_derivada)          
      
    def cifrar_clave(self,clave):        
        clave_cifrada = self._cifrar_doble(clave) 
        return self._generar_paja(clave_cifrada)
    
    def descifrar_clave(self,clave_cifrada):        
        clave_limpia = self._limpiar_paja(clave_cifrada)
        return self._descifrar_doble(clave_limpia)  
      
    def _cifrar_doble(self,clave): 
        clave_cifrada_capa_uno = self._cifrar_clave_AES256_GCM(clave)       
        return self._cifrar_clave_AES128_CBC(clave_cifrada_capa_uno)       
    
    def _descifrar_doble(self,clave_cifrada):
        clave_cifrada_capa_uno = self._descifrar_clave_AES128_CBC(clave_cifrada)              
        return self._descifrar_clave_AES256_GCM(clave_cifrada_capa_uno)
    
    def _cifrar_clave_AES128_CBC(self,clave):        
        fernet_maestra = Fernet(self._clave_maestra)        
        clave_cifrada = fernet_maestra.encrypt(clave) 
        return clave_cifrada.decode()
    
    def _descifrar_clave_AES128_CBC(self,clave_cifrada):
        fernet_maestra = Fernet(self._clave_maestra)       
        clave = fernet_maestra.decrypt(clave_cifrada.encode()) 
        return clave
    
    def _cifrar_clave_AES256_GCM(self,clave):  
        salt = os.urandom(16)
        iv = os.urandom(12) # Se aconseja para GCM en lugar de 16 ¿?
                
        kdf = self._get_kdf(salt)
        key = kdf.derive(conf.CLAVE_MAESTRA)
       
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(clave) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        tag = encryptor.tag

        return salt + iv + ciphertext + tag
    
    def _descifrar_clave_AES256_GCM(self,clave_cifrada):
        salt = clave_cifrada[:16]
        iv = clave_cifrada[16:28]
        tag = clave_cifrada[-16:]  
        clave_cifrada = clave_cifrada[28:-16]    
       
        kdf = self._get_kdf(salt)
        key = kdf.derive(conf.CLAVE_MAESTRA)

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = decryptor.update(clave_cifrada) + decryptor.finalize()

        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data
    
    def _generar_paja(self,clave):
        # TODO: complicarlo
        num = random.randint(1, 9)       
        sufijo = ''.join(random.choices(string.ascii_letters + string.digits, k=num))
        clave_sucia = str(num) + clave + sufijo
        return clave_sucia
    
    def _limpiar_paja(self,clave):        
        
        num = int(clave[0])
        return clave[1:-num]
    
    def _get_kdf(self, salt):
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # Aumentarlas en entornos de producción
            # Backend: Implementación de algoritmos para realizar operaciones criptográficas
            backend=default_backend()  # Se usa el que tiene predeterminado
        )
        
        return kdf


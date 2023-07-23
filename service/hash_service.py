import hashlib
import os
from constantes import Configuracion as conf

class HashService():
           
    # Calcula el hash del archivo
    def calcular_hash_archivo(self, ruta_archivo):
        
        tamanno = os.path.getsize(ruta_archivo)
        
        if tamanno < conf.TAMANNO_MAX_ARCHIVO_CALC_HASH:
            return self._calcular_hash_archivo_normal(ruta_archivo)

        return self._calcular_hash_archivo_grande(ruta_archivo)
    
    # Calcula el hash de una cadena
    def calcular_hash_cadena(self, nombre_archivo):
        hash_nombre_archivo = hashlib.sha256(nombre_archivo.encode()).hexdigest()
        return hash_nombre_archivo

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
    
   

    
  
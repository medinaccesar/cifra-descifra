from service.cifrado_doble_service import CifradoDobleCapa
from service.fichero_service import Fichero
from service.hash_service import HashService
from abc import ABCMeta, abstractmethod

class CifraDescifraArchivo(metaclass=ABCMeta):

    def __init__(self):
        self._cifrado_doble_capa = CifradoDobleCapa()
        self._hash_service = HashService()
        self._fichero = Fichero()       
        self._tipocifrado = ''
   
    @abstractmethod
    def cifrar_archivo(self, ruta_archivo, ruta_archivo_cifrado, callback = None):
        pass
   
    @abstractmethod
    def descifrar_archivo(self, ruta_archivo_cifrado, nombre_archivo_descifrado, callback = None):
        pass
    
    def getTipoCifrado(self):
        return self._tipocifrado
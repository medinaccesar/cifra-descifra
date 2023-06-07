import abc
import os
class ConexionBd(metaclass=abc.ABCMeta):   
    
    def __init__(self):
        self.usuario = os.getenv('USUARIO_BD')
        self.contrasenna = os.getenv('CONTRASENNA_BD')
    
    @abc.abstractmethod
    def connect(self):
        pass
    
    @abc.abstractmethod
    def crear_bd(self):
        pass
    
    @abc.abstractmethod
    def insertar_registro(self,nombre_archivo, clave_cifrada):
        pass
    
    @abc.abstractmethod    
    def obtener_clave_cifrada(self,nombre_archivo):
        pass

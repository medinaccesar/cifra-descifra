import shutil
import os
import re
from constantes import Configuracion as conf
from datetime import datetime

class Fichero():
    
    def leer_archivo(self, ruta_archivo):
        with open(ruta_archivo, 'rb') as archivo:
            contenido = archivo.read()
        return contenido

    def escribir_archivo(self, ruta_archivo, contenido):
        with open(ruta_archivo, 'wb') as archivo:
            archivo.write(contenido)

    def marca_temporal(self):
        ahora = datetime.now()
        return ahora.strftime('%y%m%d_%H%M%S')

    def quitar_ext_cifrado(self, nombre_archivo):
        partes = nombre_archivo.split(".")
        return ".".join(partes[:-1])

    def quitar_marca_temporal(self, nombre_archivo):        
        sufijo = nombre_archivo[-14:] if len(nombre_archivo) > 14 else ''
        match = re.match(r"\_\d{6}_\d{6}$", sufijo)
        if match:           
            return nombre_archivo[:-14]
        else:          
            return nombre_archivo

    def obtener_nombre_original(self, nombre_archivo):
        nombre_archivo = self.quitar_ext_cifrado(nombre_archivo)
        nombre_archivo = self.quitar_marca_temporal(nombre_archivo)
        return nombre_archivo

    def annadir_marca_temporal(self, nombre_archivo):
        marca_temporal = self.marca_temporal()
        # Se extrae la extensión del archivo
        extension = os.path.splitext(nombre_archivo)[1]
        # Se concatena la extensión con la marca temporal
        nombre_archivo = nombre_archivo[:-
                                        len(extension)] +'_'+ marca_temporal + extension
        return nombre_archivo
    

    def crear_copia_de_seguridad(self):
       
        if not os.path.exists(conf.DIR_DB_BACKUP):
            os.makedirs(conf.DIR_DB_BACKUP)        
        nombre_bd_copia = self.annadir_marca_temporal('database.db')
        shutil.copy2(conf.DIR_BD+'database.db',conf.DIR_DB_BACKUP+nombre_bd_copia)
   
    def restaurar_copia_de_seguridad(self,ruta_bd_copia): 
        
        nombre_bd_copia = self.quitar_marca_temporal(ruta_bd_copia)
        shutil.copy2(nombre_bd_copia, conf.DIR_BD+'database.db')
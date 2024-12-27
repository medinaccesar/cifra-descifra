import shutil
import os
import re
import zipfile
import json
from dotenv import dotenv_values
from constantes import Configuracion as conf
from datetime import datetime

class Fichero():
    
    def leer_archivo(self, ruta_archivo):        
        return self._leer_archivo_generico(ruta_archivo,'b')
    
    def leer_archivo_texto(self, ruta_archivo):        
        return self._leer_archivo_generico(ruta_archivo)
    
    def leer_archivo_json(self, ruta_archivo):
        if not self.existe(ruta_archivo):
            return None
        with open(ruta_archivo, 'r') as archivo:
            contenido = json.load(archivo)
        return contenido

    def escribir_archivo(self, ruta_archivo, contenido):
        self._escribir_archivo_generico(ruta_archivo, contenido,'b')
        
    def escribir_archivo_texto(self, ruta_archivo, contenido):
        self._escribir_archivo_generico(ruta_archivo, contenido)
            
    def _leer_archivo_generico(self, ruta_archivo,modo=''):
        if not self.existe(ruta_archivo):
            return None
        with open(ruta_archivo, 'r'+modo) as archivo:
            contenido = archivo.read()
        return contenido
    
    def _escribir_archivo_generico(self, ruta_archivo, contenido, modo =''):
        with open(ruta_archivo, 'w' +modo) as archivo:
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
        nombre_archivo = nombre_archivo[:-len(extension)] +'_'+ marca_temporal + extension
        return nombre_archivo
  
    def crear_copia_de_seguridad(self):
       
        if not os.path.exists(conf.DIR_DB_BACKUP):
            os.makedirs(conf.DIR_DB_BACKUP)        
        nombre_bd_copia = self.annadir_marca_temporal(conf.NOMBRE_BD)
        shutil.copy2(conf.DIR_BD+conf.NOMBRE_BD,conf.DIR_DB_BACKUP+nombre_bd_copia)
   
    def restaurar_copia_de_seguridad(self,ruta_bd_copia): 
        
        nombre_bd_copia = self.quitar_marca_temporal(ruta_bd_copia)
        shutil.copy2(nombre_bd_copia, conf.DIR_BD+conf.NOMBRE_BD)
        
    def establecer_tipo_cifrado_defecto(self, tipo_cifrado = conf.TIPO_CIFRADO_DEFECTO, ruta_env = conf.DIR_ABS+'.env'):
        if not self.existe_archivo_env():
           self.crear_archivo_env()
        env_vars = dotenv_values(ruta_env)
        env_vars['TIPO_CIFRADO'] = tipo_cifrado
        self._escribir_fichero_diccionario(ruta_env,env_vars)
   
    def existe_archivo_env(self):
        ruta_env = conf.DIR_ABS+'.env'               
        return self.existe(ruta_env)
    
    def existe(self,ruta):       
        if not os.path.isfile(ruta):
            return False       
        return True
    
    def crear_archivo_env(self):        
        ruta_env = conf.DIR_ABS+'.env'
        env_vars = {}
        env_vars['IDIOMA'] = 'es'        
        env_vars['TIPO_CIFRADO'] = conf.TIPO_CIFRADO_DEFECTO           
        self._escribir_fichero_diccionario(ruta_env,env_vars)
   
    # Comprime una lista de archivos    [uno, dos...]
    def comprimir(nombre_zip, archivos):
        with zipfile.ZipFile(nombre_zip, 'w') as zip_file:
            for archivo in archivos:
                zip_file.write(archivo)
    # descomprime o desempaqueta
    def descomprimir(nombre_zip):
        with zipfile.ZipFile(nombre_zip, 'r') as zip_file:
            zip_file.extractall()   
             
    def empaquetar(archivos, nombre_paquete):
        # Crear una carpeta temporal para almacenar los archivos
        carpeta_temporal = 'temp'
        os.makedirs(carpeta_temporal, exist_ok=True)

        # Copiar los archivos a la carpeta temporal
        for archivo in archivos:
            shutil.copy(archivo, carpeta_temporal)

        # Comprimir la carpeta temporal en un archivo .paq
        shutil.make_archive(nombre_paquete, 'zip', carpeta_temporal)

        # Eliminar la carpeta temporal
        shutil.rmtree(carpeta_temporal)
    
    def _escribir_fichero_diccionario(self,ruta,diccionario):
         with open(ruta, 'w') as archivo:
            for clave, valor in diccionario.items():
                archivo.write(f"{clave}={valor}\n")
                
    def _guardar_clave_fichero(self, data, nombre,  path = None):
        clave =json.dumps(data, indent=2)
        if path is None:
            path = conf.DIR_DOCUMENTOS + os.path.sep + nombre 
        self.escribir_archivo_texto(path, clave)
        
    def importar_clave_publica_fichero(self, ruta_archivo):
        try:
            contenido = self.leer_archivo_json(ruta_archivo)
            if not contenido:
                return None, None
            correo_electronico = contenido.get("correo_electronico")
            clave_publica = contenido.get("clave_publica")
            return clave_publica, correo_electronico
        except Exception as e:
            print(f"Error al importar clave pública: {str(e)}")
            return None, None
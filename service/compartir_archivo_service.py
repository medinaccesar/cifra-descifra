import base64
import json

from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from constantes import Configuracion as Conf
from service.cifradescifra_service import CifraDescifraArchivo
from service.cifrado_asimetrico_service import CifradoAsimetrico
from service.cifrado_doble_service import CifradoDobleCapa
from service.fichero_service import Fichero
from service.hash_service import HashService


class CompartirArchivo:
    
    def __init__(self,cifra_descifra_archivo: CifraDescifraArchivo):
                
        self._cifra_descifra_archivo = cifra_descifra_archivo
        self._cifrado_asimetrico= CifradoAsimetrico()
        self._cifrado_doble_capa = CifradoDobleCapa()
        self._hash_service = HashService()
        self._fichero = Fichero()

    def cifrar(self,ruta_archivo,cadena_correos, callback = None):
        """
        Cifra un archivo para compartirlo con múltiples destinatarios.
        
        Args:
            ruta_archivo: Ruta del archivo a cifrar
            lista_correos: Lista de correos de los destinatarios
            
        Returns:
            dict: Diccionario con el archivo cifrado y las claves cifradas para cada correo
        """
        tipo_cifrado = self._cifra_descifra_archivo.get_tipo_cifrado()
        # Cifrar el archivo
        archivo_cifrado, clave, adicional = self.cifrar_archivo(ruta_archivo)
        archivo_cifrado = base64.b64encode(archivo_cifrado).decode('utf-8')
        
        # Obtener claves públicas de los destinatarios
        conexion_bd = ConexionBdSqlite()
        claves_correos = []
        lista_correos = cadena_correos.split(',')
        for correo in lista_correos:

            clave_publica = conexion_bd.obtener_clave_publica_por_correo(correo)
            # Cifrar la clave del archivo con la clave pública del destinatario
            clave_cifrada =  base64.b64encode(self._cifrado_asimetrico.cifrar(clave, clave_publica)).decode('utf-8')

            adicional_cifrado = ''
            if tipo_cifrado == Conf.CIFRADO_AES256_GCM:
                adicional_cifrado = base64.b64encode(self._cifrado_asimetrico.cifrar(adicional, clave_publica)).decode('utf-8')
            claves_correos.append({
                "correo": correo,
                "clave_cifrada": clave_cifrada,
                "adicional_cifrado": adicional_cifrado
            })

        return {
            "tipo_cifrado": tipo_cifrado,
            "claves_correos": claves_correos,
            "archivo_cifrado": archivo_cifrado,
        }
        
    def cifrar_archivo(self, ruta_archivo):
        contenido = self._fichero.leer_archivo(ruta_archivo)
        if contenido is None:
            return False
        clave = self._cifra_descifra_archivo.crear_clave()
        adicional = ''
        if self._cifra_descifra_archivo.get_tipo_cifrado() == Conf.CIFRADO_AES256_GCM:
            self._cifra_descifra_archivo.crear_iv()
        contenido_cifrado = self._cifra_descifra_archivo.cifrar(contenido)

        if self._cifra_descifra_archivo.get_tipo_cifrado() == Conf.CIFRADO_AES256_GCM:
           adicional = self._cifra_descifra_archivo.get_adicional()
        
        return contenido_cifrado, clave, adicional

    def exportar(self,ruta_archivo,cadena_correos, callback = None):
        try:
            # obtener el nombre de la ruta de archivo
            nombre_archivo = self._fichero.obtener_nombre(ruta_archivo) + '.comp'  #TODO: a constantes
            datos = self.cifrar(ruta_archivo, cadena_correos, callback)
            self._fichero.exportar_archivo_compartido(nombre_archivo, datos)
        except Exception as e:
            print(f"Error al exportar el archivo compartido: {str(e)}")
            return False
        return True

    def importar(self, ruta_archivo, callback = None):
        conexion_bd = ConexionBdSqlite()
        clave_privada, correo_electronico = conexion_bd.obtener_clave_privada_correo()
        # Leer el archivo importado
        datos = self._fichero.leer_archivo_json(ruta_archivo)

        # Buscar el correo que coincide con el de la tabla clave_publica_clave_privada
        correo = None
        for clave_correo in datos["claves_correos"]:
            if clave_correo["correo"] ==correo_electronico:
                correo = clave_correo
                break

        if correo:
                       # Descifrar clave_cifrada y adicional_cifrado
            clave_cifrada = correo["clave_cifrada"]
            adicional_cifrado = correo["adicional_cifrado"]
            clave_descifrada = self._cifrado_asimetrico.descifrar(clave_cifrada, clave_privada)
            adicional_descifrado = self._cifrado_asimetrico.descifrar(adicional_cifrado, clave_privada)

            # Cifrar clave_descifrada y adicional_descifrado con cifrar_clave de CifradoDobleCapa
            clave_cifrada_doble_capa = self._cifrado_doble_capa.cifrar_clave(clave_descifrada)
            adicional_cifrado_doble_capa = self._cifrado_doble_capa.cifrar_clave(adicional_descifrado)
            datos_archivo =  datos["archivo_cifrado"]
            hash_archivo = self._hash_service.calcular_hash_cadena(ruta_archivo)
            # Guardar los datos en la tabla de claves
            conexion_bd.insertar_registro(hash_archivo, clave_cifrada_doble_capa, adicional_cifrado_doble_capa,
                                      datos["tipo_cifrado"])
            return True
        else:
            print("No se encontró el correo en el archivo importado")
            return False
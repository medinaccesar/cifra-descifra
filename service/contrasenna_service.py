from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from constantes import Configuracion as conf

class ContrasennaService():
    
    def establecer_contrasenna(self, clave_cifrada):  
        conexion_bd = ConexionBdSqlite()      
        if not self.obtener_requiere_clave_aplicacion():           
            conexion_bd.insertar_requiere_clave_aplicacion(clave_cifrada)
        else:     
            conexion_bd.actualizar_requiere_clave_aplicacion(clave_cifrada)            
            self.obtener_requiere_clave_aplicacion()
    def obtener_requiere_clave_aplicacion(self):
        conexion_bd = ConexionBdSqlite()
        requiere_clave, clave_aplicacion = conexion_bd.obtener_requiere_clave_aplicacion()
        return requiere_clave, clave_aplicacion
    
    def desestablecer_contrasenna(self, clave_aplicacion, clave_usuario):
        conexion_bd = ConexionBdSqlite()     
        if clave_aplicacion == clave_usuario:
            conexion_bd.desestablecer_clave_aplicacion()
            return True
        return False
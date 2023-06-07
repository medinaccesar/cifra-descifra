import sqlite3
from conexion_bd.conexion_bd import ConexionBd
from constantes import Configuracion as conf
class ConexionBdSqlite(ConexionBd):   
    
    def connect(self):
        conn = sqlite3.connect(conf.DIR_BD+'database.db')  
        cursor = conn.cursor()      
        return conn, cursor
    
    def crear_bd(self):
        conn, cursor = self.connect()               
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS claves (
                            hash_archivo TEXT PRIMARY KEY,
                            clave_cifrada TEXT NOT NULL
                        )
                    ''')
        conn.commit()
        conn.close()
        
    def insertar_registro(self,hash_archivo, clave_cifrada):
        conn, cursor = self.connect()        
        cursor.execute('INSERT INTO claves (hash_archivo, clave_cifrada) VALUES (?, ?)', (hash_archivo, clave_cifrada))
        conn.commit()
        conn.close()
        
    def obtener_clave_cifrada(self,hash_archivo):
        conn, cursor = self.connect()     
        cursor.execute('SELECT clave_cifrada FROM claves WHERE hash_archivo = ?', (hash_archivo,))
        fila = cursor.fetchone()
        clave_cifrada =  None if fila is None else fila[0]         
        conn.close()
        return clave_cifrada
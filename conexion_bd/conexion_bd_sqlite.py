import sqlite3
from conexion_bd.conexion_bd import ConexionBd
from constantes import Configuracion as conf
# TODO crear repositorios específicos o usar un ORM (piccolo)
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
                            clave_cifrada TEXT NOT NULL, 
                            adicional_cifrado TEXT NOT NULL,
                            tipo_cifrado TEXT NOT NULL
                        )
                    ''')
                
                        
        cursor.execute('''CREATE TABLE IF NOT EXISTS clave_publica_privada (
                    id INTEGER PRIMARY KEY,
                    clave_publica TEXT NOT NULL,
                    clave_privada TEXT NOT NULL)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS opciones (
                    id INTEGER PRIMARY KEY,
                    requiere_clave_aplicacion INTEGER CHECK(requiere_clave_aplicacion IN (0, 1)) NOT NULL DEFAULT 0,
                    clave_aplicacion TEXT  NULL)''')
        conn.commit()
        conn.close()
        
    def insertar_registro(self,hash_archivo, clave_cifrada, adicional_cifrado, tipo_cifrado):
        conn, cursor = self.connect()        
        cursor.execute('INSERT INTO claves (hash_archivo, clave_cifrada, adicional_cifrado, tipo_cifrado) VALUES (?, ?, ?, ?)', (hash_archivo, clave_cifrada, adicional_cifrado, tipo_cifrado))
        conn.commit()
        conn.close()
        
    def obtener_clave_cifrada(self,hash_archivo):
        conn, cursor = self.connect() 
       
        cursor.execute('SELECT clave_cifrada FROM claves WHERE hash_archivo = ?', (hash_archivo,))
     
        fila = cursor.fetchone()
    
        clave_cifrada =  None if fila is None else fila[0]         
        conn.close()
        return clave_cifrada
    
    def obtener_adicional_cifrado(self,hash_archivo):
        conn, cursor = self.connect()     
        cursor.execute('SELECT adicional_cifrado FROM claves WHERE hash_archivo = ?', (hash_archivo,))
        fila = cursor.fetchone()
        adicional_cifrado =  None if fila is None else fila[0]         
        conn.close()
        return adicional_cifrado
    
    def obtener_clave_cifrada_adicional_cifrado(self,hash_archivo):
        conn, cursor = self.connect()     
        cursor.execute('SELECT clave_cifrada, adicional_cifrado FROM claves WHERE hash_archivo = ?', (hash_archivo,))
        fila = cursor.fetchone()
        clave_cifrada =  None if fila is None else fila[0]         
        adicional_cifrado =  None if fila is None else fila[1]         
        conn.close()
        return clave_cifrada, adicional_cifrado
    
    def obtener_clave_publica_clave_privada(self):
        conn, cursor = self.connect()     
        cursor.execute('SELECT clave_publica,clave_privada  FROM clave_publica_privada where id = ?', ('0'))
        fila = cursor.fetchone()
        clave_publica =  None if fila is None else fila[0]         
        clave_privada =  None if fila is None else fila[1]         
        conn.close()
        return clave_publica, clave_privada
    
    def insertar_clave_publica_clave_privada(self, clave_publica, clave_privada):
        conn, cursor = self.connect()     
        cursor.execute('INSERT INTO clave_publica_privada (id, clave_publica,clave_privada) VALUES (?, ?, ?)', ('0', clave_publica, clave_privada))
        conn.commit()
        conn.close()
        
    def obtener_requiere_clave_aplicacion(self):
        conn, cursor = self.connect()     
        cursor.execute('SELECT requiere_clave_aplicacion,clave_aplicacion  FROM opciones where id = ?', ('0'))
        fila = cursor.fetchone()
        requiere_clave_aplicacion =  None if fila is None else fila[0]         
        clave_aplicacion =  None if fila is None else fila[1]         
        conn.close()
        return requiere_clave_aplicacion,clave_aplicacion
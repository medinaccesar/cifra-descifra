import sqlite3
from conexion_bd.conexion_bd import ConexionBd
from constantes import Configuracion as conf
# TODO Crear repositorios específicos o usar un ORM (piccolo)
class ConexionBdSqlite(ConexionBd):   
    
    def connect(self):
        conn = sqlite3.connect(conf.DIR_BD+conf.NOMBRE_BD)  
        cursor = conn.cursor()      
        return conn, cursor
    
    def crear_bd(self,privada, publica):
        conn, cursor = self.connect()               
        self._crear_tablas(cursor)
        self._poblar_tablas(cursor, privada, publica)
        conn.commit()
        conn.close()
    
    def _poblar_tablas(self,cursor, privada, publica):
          cursor.execute('INSERT INTO clave_publica_privada (id, clave_publica, clave_privada, correo_electronico) VALUES (?, ?, ?, ?)', ('1', publica, privada, None))
            
    def _crear_tablas(self, cursor):
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
                    clave_privada TEXT NOT NULL,
                    correo_electronico TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS claves_publicas (
                    id INTEGER PRIMARY KEY,
                    clave_publica TEXT NOT NULL,
                    correo TEXT NOT NULL,                    
                    descripcion TEXT  NULL                    
                    )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS opciones (
                    id INTEGER PRIMARY KEY,
                    requiere_clave_aplicacion INTEGER CHECK(requiere_clave_aplicacion IN (0, 1)) NOT NULL DEFAULT 0,
                    clave_aplicacion TEXT  NULL)''')
        
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
    
    def obtener_clave_publica_correo(self):
        conn, cursor = self.connect()     
        cursor.execute('SELECT clave_publica, correo_electronico FROM clave_publica_privada where id = ?', ('1',))
        fila = cursor.fetchone()
        clave_publica = None if fila is None else fila[0]
        correo_electronico = None if fila is None else fila[1]
        conn.close()
        return clave_publica, correo_electronico

    def obtener_clave_publica_clave_privada(self):
        conn, cursor = self.connect()     
        cursor.execute('SELECT clave_publica,clave_privada  FROM clave_publica_privada where id = ?', ('1'))
        fila = cursor.fetchone()
        clave_publica =  None if fila is None else fila[0]         
        clave_privada =  None if fila is None else fila[1]         
        conn.close()
        return clave_publica, clave_privada   
    
    def obtener_clave_publica(self):
        conn, cursor = self.connect()     
        cursor.execute('SELECT clave_publica  FROM clave_publica_privada where id = ?', ('1'))
        fila = cursor.fetchone()
        clave_publica =  None if fila is None else fila[0]  
        conn.close()
        return clave_publica
        
    def obtener_requiere_clave_aplicacion(self):
        conn, cursor = self.connect()     
        cursor.execute('SELECT requiere_clave_aplicacion,clave_aplicacion  FROM opciones where id = ?', ('1'))
        fila = cursor.fetchone()       
        requiere_clave_aplicacion =  None if fila is None else fila[0]         
        clave_aplicacion =  None if fila is None else fila[1]         
        conn.close()
        return requiere_clave_aplicacion,clave_aplicacion
    
    def insertar_requiere_clave_aplicacion(self, clave_cifrada):
        conn, cursor = self.connect()     
        cursor.execute('INSERT INTO opciones (id, requiere_clave_aplicacion, clave_aplicacion) VALUES (?, ?, ?)', ('1','1', clave_cifrada))
        conn.commit()
        conn.close()
    
    def actualizar_requiere_clave_aplicacion(self, clave_cifrada):
        conn, cursor = self.connect()     
        sentencia =  "UPDATE opciones SET requiere_clave_aplicacion = ?, clave_aplicacion = ? WHERE id = ?"
        cursor.execute(sentencia, ('1',clave_cifrada , '1'))
        conn.commit()
        conn.close()
        
    def desestablecer_clave_aplicacion(self):
        conn, cursor = self.connect()     
        sentencia =  "UPDATE opciones SET requiere_clave_aplicacion = ?, clave_aplicacion = ? WHERE id = ?"
        cursor.execute(sentencia, ( '0', None,'1'))
        conn.commit()
        conn.close()

    def actualizar_correo_electronico(self, correo):
        conn, cursor = self.connect()
        cursor.execute('UPDATE clave_publica_privada SET correo_electronico = ? WHERE id = ?', (correo, '1'))
        conn.commit()
        conn.close()

    def insertar_clave_publica(self, clave_publica, correo, descripcion=None):
        conn, cursor = self.connect()
        cursor.execute('INSERT INTO claves_publicas (clave_publica, correo, descripcion) VALUES (?, ?, ?)', 
                      (clave_publica, correo, descripcion))
        conn.commit()
        conn.close()

    def existe_correo(self, correo):
        conn, cursor = self.connect()
        cursor.execute('SELECT COUNT(*) FROM claves_publicas WHERE correo = ?', (correo,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def actualizar_clave_publica(self, clave_publica, correo):
        conn, cursor = self.connect()
        cursor.execute('UPDATE claves_publicas SET clave_publica = ? WHERE correo = ?', 
                      (clave_publica, correo))
        conn.commit()
        conn.close()

    def obtener_listado_claves_publicas(self):
        conn, cursor = self.connect()
        cursor.execute('SELECT correo, descripcion FROM claves_publicas')
        claves = cursor.fetchall()
        conn.close()
        return claves
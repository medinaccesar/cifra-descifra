
from utils.espannol_string_argparse import *
import argparse
from utils.locale_manager import _,p
from dotenv import load_dotenv
from gui.gui import Gui
from constantes import Configuracion as conf
from service.contrasenna_service import ContrasennaService
from service.cifrado_doble_service import CifradoDobleCapa
from service.cifrado_asimetrico_service import CifradoAsimetrico
from service.tipos_cifrado.cifrado_AES128_CBC_service import CifraDescifraArchivoAES128CBC
from service.tipos_cifrado.cifrado_AES256_GCM_service import CifraDescifraArchivoAES256GCM
from service.tipos_cifrado.cifrado_XChaCha20_Poly1305_service import CifraDescifraArchivoXChachaPoly
from service.fichero_service import Fichero
from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from utils.barra_progreso import BarraProgresoConsola

class CifraDescifra():

    def __init__(self):
               
        self._cifrado_doble_capa  = CifradoDobleCapa()
        self._cifrado_asimetrico  = CifradoAsimetrico()
        self._contrasenna_service = ContrasennaService()
        self._fichero = Fichero()
        self._instanciar_tipo_cifrado()
        self._comprobar_bd()
       
        self._procesar_argumentos()

    def _comprobar_bd(self):
        if not self._fichero.existe(conf.DIR_BD + conf.NOMBRE_BD):
            conexion_bd = ConexionBdSqlite()   
            #TODO: generar la clave maestra y guardarla en bd en lugar de en conf
            privada, publica = self._cifrado_asimetrico.generar_claves_cifrada()         
            conexion_bd.crear_bd(privada, publica)          
            

    # Se ejecuta con entorno gráfico
    def _ejecutar_gui(self):
        
        gui = Gui()
        gui.set_cifra_descifra_archivo(self._cifra_descifra_archivo)
        gui.mainloop()

    # Se ejecuta en modo consola
    def _ejecutar_modo_consola(self, args):

        print(_('Se ejecuta en modo consola.'),'\n')

        if args.cifrar is not None:
            barra_progreso = BarraProgresoConsola(100)
            nombre_archivo, nombre_archivo_cifrado = args.cifrar
            #TODO: comprobar que existe el archivo
            if  self._cifra_descifra_archivo.cifrar_archivo(
                nombre_archivo, nombre_archivo_cifrado,barra_progreso.dibuja_bp):
                print(_('El archivo se ha cifrado correctamente.'),'\n')
            else:
                print(_('El archivo no se ha podido cifrar.'),'\n')    
            
        elif args.descifrar is not None:
            barra_progreso = BarraProgresoConsola(100)
            nombre_archivo_cifrado, nombre_archivo_descifrado = args.descifrar
            #TODO: comprobar que existe el archivo
            if  self._cifra_descifra_archivo.descifrar_archivo(
                nombre_archivo_cifrado, nombre_archivo_descifrado,barra_progreso.dibuja_bp):
                print(_('El archivo se ha descifrado correctamente.'),'\n')
            else:
                print(_('El archivo no se ha podido descifrar.'),'\n')
            
        elif args.clave is not None and args.clave is not False:            
            self._establecer_contrasenna()
            print(_('La contraseña se ha establecido correctamente.'),'\n') 
        elif args.quitar_clave is not None and args.quitar_clave is not False: 
            if self._desestablecer_contrasenna():
                print(_('La contraseña se ha desestablecido correctamente.'),'\n') 
        elif args.copiar is not None and args.copiar is not False:            
            self._fichero.crear_copia_de_seguridad()
            print(_('La base de datos se ha copiado correctamente.'),'\n') 
        
        elif args.restaurar is not None and  args.restaurar is not False:
            action = input(_('Al restaurar se borrará la base de datos actual, ¿está seguro? (s/n)'))
            if action == 's' or action == 'S':
                nombre_archivo_bd = args.restaurar
                print(nombre_archivo_bd)
                if os.path.exists(nombre_archivo_bd):
                    self._fichero.restaurar_copia_de_seguridad(nombre_archivo_bd)
                    print(_('La base de datos se ha restaurado correctamente.'),'\n')  
                else: print(_(f'El archivo {nombre_archivo_bd} no existe.'),'\n')    
        elif args.tipo_cifrado is not None and args.tipo_cifrado is not False:            
           self._establecer_tipo_cifrado()       
        elif args.info is not None and args.info is not False:  
                      
            if not self._fichero.existe_archivo_env():
                self._fichero.crear_archivo_env()               
            load_dotenv()      
            print(_('Opciones establecidas:'),'\n')              
            print('IDIOMA: ', os.getenv('IDIOMA'))
            print('TIPO_CIFRADO: ',os.getenv('TIPO_CIFRADO'))    
            clave_establecida = _('No')
            requiere_clave, clave_aplicacion = self._contrasenna_service.obtener_requiere_clave_aplicacion()
            if  requiere_clave:
                clave_establecida = _('Sí')  
            print('Requiere clave: ',clave_establecida,'\n')
                    
        elif args.exportar_clave is not None and args.exportar_clave is not False:
           if self._exportar_clave_publica():
                print(_('La clave pública se ha exportado correctamente.'),'\n')  
           else:  print(_('No hay ninguna clave pública para exportar'),'\n')   
        else:
            print(_('No se especificó ninguna opción'))
            
    # Se ejecuta en modo de consola guiado
    def _ejecutar_modo_guiado(self):
        
        accion = input(
            _('¿Desea cifrar o descifrar un archivo? (cifrar/descifrar) o (c/d): '))

        if accion == 'cifrar' or accion == 'c':
          
            nombre_archivo = input(
                _('Introduzca el nombre del archivo a cifrar: '))
            nombre_archivo_cifrado = input(
                _('Introduzca el nombre del archivo cifrado que se va a generar: '))
            barra_progreso = BarraProgresoConsola(100)
            self._cifra_descifra_archivo.cifrar_archivo(
                nombre_archivo, nombre_archivo_cifrado,barra_progreso.dibuja_bp)
            print(_('El archivo se ha cifrado correctamente.'))

        elif accion == 'descifrar' or accion == 'd':
            nombre_archivo_cifrado = input(
                _('Introduce el nombre del archivo cifrado a descifrar: '))
            nombre_archivo_descifrado = input(
                _('Introduce el nombre del archivo descifrado que se va a generar: '))
            barra_progreso = BarraProgresoConsola(100)
            self._cifra_descifra_archivo.descifrar_archivo(
                nombre_archivo_cifrado, nombre_archivo_descifrado,barra_progreso.dibuja_bp)
            print(_('El archivo se ha descifrado correctamente.'))
        else:
            print(_('La acción introducida no es válida'))

    def _instanciar_tipo_cifrado(self):       
        load_dotenv() 
        tipo_cifrado =  os.getenv('TIPO_CIFRADO', conf.TIPO_CIFRADO_DEFECTO)
        
        tipos_cifrado = {
            conf.CIFRADO_AES128_CBC: lambda: CifraDescifraArchivoAES128CBC(),
            conf.CIFRADO_AES256_GCM: lambda: CifraDescifraArchivoAES256GCM(),
            conf.CIFRADO_CHACHA20_POLY1305: lambda: CifraDescifraArchivoXChachaPoly()
        }

        self._cifra_descifra_archivo = tipos_cifrado.get(tipo_cifrado, lambda: CifraDescifraArchivoAES256GCM())()
       
           
    def _establecer_tipo_cifrado(self):
        
        tipo_cifrado = input('\n'+
            _('¿Elija el tipo de cifrado? (AES128_CBC/AES256_GCM/XChaCha20_Poly1305) o (c/g/x): '))
        
        tipos_cifrado = {
            'c': conf.CIFRADO_AES128_CBC,
            'g': conf.CIFRADO_AES256_GCM,
            'x': conf.CIFRADO_CHACHA20_POLY1305
        }
        tipo_cifrado = tipos_cifrado.get(tipo_cifrado, conf.TIPO_CIFRADO_DEFECTO)
        self._fichero.establecer_tipo_cifrado_defecto(tipo_cifrado)    
    
    def _preguntar_contrasenna(self):
        requiere_clave, clave_aplicacion = self._contrasenna_service.obtener_requiere_clave_aplicacion()        
        if requiere_clave:
            contrasenna = input( _('Intoduzca la contraseña: '))
            contrasenna_descifrada = self._cifrado_doble_capa.descifrar_clave(clave_aplicacion)            
            if not contrasenna_descifrada.decode() == contrasenna:            
                print(_('La contraseña es incorrecta'))
                exit()     
    def _desestablecer_contrasenna(self):
        print()
        print(_('Se desestablecerá la contraseña de inicio'),'\n')
        res = False        
        requiere_clave, clave_aplicacion = self._contrasenna_service.obtener_requiere_clave_aplicacion()        
        if requiere_clave:                 
            clave =  self._cifrado_doble_capa.descifrar_clave(clave_aplicacion)
            contrasenna = input( _('Para desestablecerla intoduzca antes la contraseña: '))
            if self._contrasenna_service.desestablecer_contrasenna(contrasenna,clave.decode()):            
                res = True
            else:
                print(_('La contraseña es incorrecta'))  
        else:
             print(_('No hay contraseña que desestablecer'))
        return res  
    
    def _establecer_contrasenna(self):        
        print(_('Se establecerá una contraseña de inicio'),'\n')
        while True:
            contrasenna = input( _('Intoduzca la contraseña: '))
            clave = input( _('Repita la contraseña: '))
            if contrasenna!=clave:
                print(_('Las contraseñas no coinciden'))
            else: break    
        clave_cifrada =  self._cifrado_doble_capa.cifrar_clave(bytes(contrasenna, "utf-8"))
        self._contrasenna_service.establecer_contrasenna(clave_cifrada)          
    def _exportar_clave_publica(self):        
        print(_('Se exportará a un fichero la clave pública '),'\n')
        conexion_bd = ConexionBdSqlite() 
        clave_publica  = conexion_bd.obtener_clave_publica()    
        if clave_publica is not None:
            self._cifrado_asimetrico.exportar_clave_publica_fichero(clave_publica)            
            return True         
        return False   

    def _get_parser(self):
        
        parser = argparse.ArgumentParser(
            description=conf.NOMBRE_AP+" "+str(conf.VERSION))  # formatter_class=CustomHelpFormatter
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-c', '--cifrar', nargs=2,
                           metavar=(_('ARCHIVO'), _('ARCHIVO_CIFRADO')), help='Cifrar archivo')
        group.add_argument('-d', '--descifrar', nargs=2, metavar=(
            _('ARCHIVO_CIFRADO'), _('ARCHIVO_DESCIFRADO')), help=_('Descifrar archivo'))
        group.add_argument('-g', '--gui', action='store_true',
                           help=_('Se ejecuta el entorno gráfico'))
        group.add_argument(
            '-a', '--asistido', action='store_true', help=_('Se ejecuta el modo guiado'))
        group.add_argument(
            '-b', '--copiar', action='store_true', help=_('Hace una copia de la base de datos'))
        group.add_argument(
            '-r', '--restaurar', type=str,
                           metavar=_('ARCHIVO_COPIA'), help=_('Restaura una copia de la base de datos'))
        group.add_argument(
            '-C', '--clave', action='store_true', help=_('Establece una contraseña para ejecutar el programa'))
        group.add_argument(
            '-Q', '--quitar-clave', action='store_true', help=_('Desestablece la contraseña'))
        group.add_argument(
            '-t', '--tipo-cifrado', action='store_true', help=_('Selecciona el tipo de cifrado por defecto'))
        group.add_argument(
            '-E', '--exportar-clave', type=str,
                           metavar=_('NOMBRE_ARCHIVO'), help=_('Exporta tu clave pública'))
        group.add_argument('-cc', '--compartir', nargs=argparse.ONE_OR_MORE, metavar=(
            _('ARCHIVO'), _('CORREO_1, CORREO_2')), help=_('Cifrar archivo para compartirlo'))
        group.add_argument(
            '-ic', '--importar-clave', type=str,
                           metavar=_('ARCHIVO_CLAVE'), help=_('Importa una clave pública de otro usuario'))
        group.add_argument(
            '-l', '--listar-claves', action='store_true', help=_('Lista los correos de las claves públicas'))
        group.add_argument(
            '-i', '--info', action='store_true', help=_('Muesta las opciones establecidas'))
        parser.add_argument('--version', action='version', version='%(prog)s ' +
                            conf.VERSION, help=_('Muestra la versión del programa'))

        return parser

    def _procesar_argumentos(self):
        parser = self._get_parser()       
        args = parser.parse_args()
        if args.gui:
            # TODO: resolver dónde preguntar la contraseña en GUI
            #self._ejecutar_gui()
            print(_('La opción GUI no está implementada aún'))
        else:
            self._preguntar_contrasenna()
            # self._preguntar_tipo_cifrado()
            if args.asistido:
                self._ejecutar_modo_guiado()       
            else:                
                self._ejecutar_modo_consola(args)



if __name__ == "__main__":
     
    CifraDescifra()

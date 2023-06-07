
from utils.espannol_string_argparse import *
import argparse
from utils.locale_manager import _
from gui.gui import Gui
from service.cifradescifra_service import CifraDescifraArchivo
from conexion_bd.conexion_bd_sqlite import ConexionBdSqlite
from constantes import Configuracion as conf


class CifraDescifra():

    def __init__(self):
        
        self._cifra_descifra_archivo = CifraDescifraArchivo()
        self._comprobar_bd()
        parser = self._get_parser()
        self._procesar_argumentos(parser)

    def _comprobar_bd(self):
        
        conexion_bd = ConexionBdSqlite()
        # Sólo si no hay BD la crea
        conexion_bd.crear_bd()

    # Se ejecuta con entorno gráfico
    def _ejecutar_gui(self):
        
        gui = Gui()
        gui.mainloop()

    # Se ejecuta en modo consola
    def _ejecutar_modo_consola(self, args):

        print(_('Se ejecuta en modo consola'))

        if args.cifrar is not None:
            nombre_archivo, nombre_archivo_cifrado = args.cifrar
            self._cifra_descifra_archivo.cifrar_archivo(
                nombre_archivo, nombre_archivo_cifrado)
            print(_('El archivo se ha cifrado correctamente.'))
        elif args.descifrar is not None:
            nombre_archivo_cifrado, nombre_archivo_descifrado = args.descifrar
            self._cifra_descifra_archivo.descifrar_archivo(
                nombre_archivo_cifrado, nombre_archivo_descifrado)
            print(_('El archivo se ha descifrado correctamente.'))
        else:
            print(_('No se especificó ninguna opción'))
            
    # Se ejecuta en modo de consola guiado
    def _ejecutar_modo_guiado(self):

        accion = input(
            _('¿Desea cifrar o descifrar un archivo? (cifrar/descifrar) o (c/d): '))

        if accion == 'cifrar' or accion == 'c':
            nombre_archivo = input(
                'Introduzca el nombre del archivo a cifrar: ')
            nombre_archivo_cifrado = input(
                'Introduzca el nombre del archivo cifrado que se va a generar: ')
            self._cifra_descifra_archivo.cifrar_archivo(
                nombre_archivo, nombre_archivo_cifrado)
            print('El archivo se ha cifrado correctamente.')

        elif accion == 'descifrar' or accion == 'd':
            nombre_archivo_cifrado = input(
                _('Introduce el nombre del archivo cifrado a descifrar: '))
            nombre_archivo_descifrado = input(
                _('Introduce el nombre del archivo descifrado que se va a generar: '))
            self._cifra_descifra_archivo.descifrar_archivo(
                nombre_archivo_cifrado, nombre_archivo_descifrado)
            print(_('El archivo se ha descifrado correctamente.'))
        else:
            print(_('La acción introducida no es válida'))

    def _get_parser(self):
        
        parser = argparse.ArgumentParser(
            description=conf.NOMBRE_AP+" "+str(conf.VERSION))  # formatter_class=CustomHelpFormatter
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-c', '--cifrar', nargs=2,
                           metavar=('ARCHIVO', 'ARCHIVO_CIFRADO'), help='Cifrar archivo')
        group.add_argument('-d', '--descifrar', nargs=2, metavar=(
            'ARCHIVO_CIFRADO', 'ARCHIVO_DESCIFRADO'), help=_('Descifrar archivo'))
        group.add_argument('-g', '--gui', action='store_true',
                           help=_('Se ejecuta el entorno gráfico'))
        group.add_argument(
            '-a', '--asesorado', action='store_true', help=_('Se ejecuta el modo guiado'))
        parser.add_argument('--version', action='version', version='%(prog)s ' +
                            conf.VERSION, help=_('Muestra la versión del programa'))

        return parser

    def _procesar_argumentos(self, parser):
        args = parser.parse_args()
        if args.gui:
            self._ejecutar_gui()
        elif args.asesorado:
            self._ejecutar_modo_guiado()
        else:
            self._ejecutar_modo_consola(args)


if __name__ == "__main__":

    CifraDescifra()

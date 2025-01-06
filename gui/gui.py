import threading
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import tkinter.messagebox as tkmb
from tkinter.ttk import Progressbar
from tkinter import PhotoImage
from service.fichero_service import Fichero
from utils.locale_manager import _
from service.tipos_cifrado.cifrado_AES256_GCM_service import CifraDescifraArchivoAES256GCM
from constantes import Configuracion as conf

class Gui(Frame):
    
    def __init__(self, master=None):
        
        super().__init__(master)
        
        self._cifra_descifra_archivo = CifraDescifraArchivoAES256GCM()
        self._fichero = Fichero()
        self._ruta_archivo = ''
        self.master.title(conf.NOMBRE_AP) 
        self.master.geometry("800x500")
        # p1 = PhotoImage(file = conf.DIR_IMA+'logo.png')  
        # self.master.iconphoto(self, p1)
        self.addTitulo()
        self.addControles()
        self.addMenu()
        
        self.pack()
    def set_cifra_descifra_archivo(self,cifra_descifra_archivo):    
        self._cifra_descifra_archivo = cifra_descifra_archivo
    def addMenu(self):
        menu = Menu(self)
       
        file_menu = Menu(menu, tearoff=0)        
        file_menu.add_command(label=_("Abrir"), command=self.seleccionar_archivo, accelerator='Ctrl+A' )       
        
        menu_interno = Menu(file_menu, tearoff=0)
        menu_interno.add_command(label=_("Cifrar"), command=self.hilo_cifrar_archivo)
        menu_interno.add_command(label=_("Descifrar"), command=self.hilo_descifrar_archivo)
        
        file_menu.add_cascade(label=_("Ejecutar"), menu=menu_interno)
        file_menu.add_separator()
        file_menu.add_command(label=_("Salir"), command=self.quit)
        menu.add_cascade(label=_("Archivo"), menu=file_menu)       

        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label=_("Acerca de..."), 
                              command=lambda:  tkmb.showinfo(title=_('Acerca de...'), 
                                                             message=conf.NOMBRE_AP+' '+conf.VERSION,icon='info', detail=_(conf.DESCRIPCION_APP)+'\n\n'+conf.CREDITOS+', 2023\nVillalmanzo, (España)'))
        menu.add_cascade(label=_("Ayuda"), menu=help_menu)
        
        #
        # Establece la barra de menú como la barra de menú principal
        self.master.config(menu=menu)
            
    def addTitulo(self):   
        # Crear el frame que contiene los controles 
        controles_frame = Frame(self,highlightbackground="white", highlightthickness=2)
        controles_frame.pack(fill=BOTH,pady=(10,20)) 
        titulo = Label( controles_frame, text=_(conf.DESCRIPCION_APP))
        font_style = Font(family="Lucida Grande", size=20)
        titulo.config(font=font_style)

        titulo.pack(pady=5)
        descripcion = Label( controles_frame, text=_('Selecciona el archivo y la operación a realizar'))
        descripcion.pack(pady=5)
        
    def addControles(self):
                
        # Crear el marco que contiene los controles de opción
        self.options_frame = Frame(self)
        self.options_frame.pack(pady=10)
        operacion_lb = Label( self.options_frame, text=_('Operación'))
        operacion_lb.pack(side="top",pady=5)
        # Crear las variables que almacenan el estado de las opciones
        self.option_var = StringVar(value="cifrar")
         # Crear los radiobuttons para cada opción
        self.option1_radiobutton = Radiobutton(self.options_frame, text=_("Cifrar"), variable=self.option_var, value="cifrar")
        self.option2_radiobutton = Radiobutton(self.options_frame, text=_("Descifrar"), variable=self.option_var, value="descifrar")
        self.option_var.set("cifrar")
        # Posicionar los radiobuttons en la ventana
        self.option1_radiobutton.pack(side="left",pady=10)
        self.option2_radiobutton.pack(side="left",pady=10)
               
        
        self.archivo_frame = Frame(self)
        self.archivo_frame.pack(pady=10)
        boton_seleccionar_archivo = Button(self.archivo_frame, text=_('Selecciona'), command=self.seleccionar_archivo)
        self.label_archivo = Label(self.archivo_frame, text='',highlightbackground="grey", highlightthickness=2)
       
        boton_seleccionar_archivo.pack(side="left",pady=10)
        self.label_archivo.pack(side="left",pady=10,fill=BOTH,expand=True)
                       
        #Barra de progreso:
        self.progress_bar = Progressbar(self, orient="horizontal", length=300, mode="determinate")        
        self.progress_bar.pack(pady=20, fill="x")
                       
        self.boton_ejecutar = Button(self, text=_('Ejecutar'), command=self.ejecutar)
        self.boton_ejecutar.pack()
     
        # Se añade un campo de texto para mostrar el resultado de la operación
        self.resultado = Label(self, text='...')
        self.resultado.pack(pady=20)   
    
    
    def ejecutar(self):
        
        self.inicializar_controles()
        if self.option_var.get() =="cifrar":                     
            self.hilo_cifrar_archivo()
        elif self.option_var.get() =="descifrar":              
            self.hilo_descifrar_archivo() 
            
    def hay_archivo_seleccionado(self):        
        if self._ruta_archivo == '':
            return False
        return True        
        
    def cifrar_archivo(self):
        if not self.hay_archivo_seleccionado():
            self.resultado['text'] = _('No hay un archivo seleccionado')
        else:    
          
            self.progress_bar["value"] = 10
            nombre_archivo = self._ruta_archivo   
            marca_temporal = self._fichero.marca_temporal()      
            nombre_archivo_cifrado = nombre_archivo+'_'+marca_temporal+conf.EXT_ARCHIVO_CIFRADO
            self._cifra_descifra_archivo.cifrar_archivo(nombre_archivo, nombre_archivo_cifrado, self.barra_progreso_callback)
            self.resultado['text'] = _('El archivo se ha cifrado correctamente.')
        

    def descifrar_archivo(self):
        if not self.hay_archivo_seleccionado():
            self.resultado['text'] = _('No hay un archivo seleccionado')
        else: 
            self.progress_bar["value"] = 10            
            nombre_archivo_cifrado = self._ruta_archivo             
            nombre_archivo_descifrado = self._fichero.obtener_nombre_original(nombre_archivo_cifrado)
            nombre_archivo_descifrado = self._fichero.annadir_marca_temporal(nombre_archivo_descifrado)
            self._cifra_descifra_archivo.descifrar_archivo(nombre_archivo_cifrado, nombre_archivo_descifrado, self.barra_progreso_callback)
            self.resultado['text'] = _('El archivo se ha descifrado correctamente.')          
            
    def barra_progreso_callback(self, valor = 10 ):
        # TODO: Mejorar transición..     
        if self.progress_bar['value'] < 100:
            self.progress_bar['value'] += valor           
        
    def hilo_descifrar_archivo(self): 
        threading.Thread(target=self.descifrar_archivo).start()    
         
    def hilo_cifrar_archivo(self): 
        threading.Thread(target=self.cifrar_archivo).start()     
            
    def seleccionar_archivo(self):
        # Muestra el diálogo de selección de archivos
        self.inicializar_controles()
        self._ruta_archivo = askopenfilename() # initialdir=conf.DIR_DOCUMENTOS
        self.label_archivo['text']=self._ruta_archivo 
        
    def inicializar_controles(self):
        self.progress_bar.stop()   
        self.resultado['text']=''

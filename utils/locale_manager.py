import gettext
import locale
import os
from dotenv import load_dotenv
load_dotenv() 
localedir = 'locale'
lang =  os.getenv('IDIOMA')

if lang is None:
    # Configura el idioma de la aplicación según la configuración del sistema
    locale.setlocale(locale.LC_ALL, '')
    lang, encoding = locale.getlocale()

# Carga los archivos de traducción para el idioma configurado
t = gettext.translation('programa', localedir, [lang], fallback=True)
_ = t.gettext

def p(cadena):
    print(_(cadena))
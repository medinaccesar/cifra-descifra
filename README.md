# cifra-descifra
Permite cifrar y descifrar archivos, puede ejecutarse en modo consola, en modo guiado o en modo gráfico. Por defecto en español pero admite otros idiomas.
El cifrado se hace con una clave única, (para cada archivo), que se genera para cada operación de cifrado, estas claves se gestionan internamente y están a su vez cifradas con una clave maestra configurable.

# Requisitos
 Para las variables de entorno «python-dotenv», y si se quiere usar la interfaz gráfica «tkinter».        

# Uso
```
Uso: cifradescifra.py [-h] [-c ARCHIVO ARCHIVO_CIFRADO | -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO | -g | -a] [--version]

Cifradescifra 1.0.0

argumentos opcionales:
  -h, --help            muestra este mensaje de ayuda y sale
  -c ARCHIVO ARCHIVO_CIFRADO, --cifrar ARCHIVO ARCHIVO_CIFRADO  Cifra el archivo                      
  -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO, --descifrar ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO Descifra el archivo                     
  -g, --gui             Se ejecuta el entorno gráfico
  -a, --asesorado       Se ejecuta el modo guiado
  --version             Muestra la versión del programa
```
# Traducciones / Translations
Se puede usar como base ./locales/programa.po y con «poedit» se rellenan las traducciones y se compila para generar el archivo «programa.mo».  Ambos archivos se colocan dentro de la carpeta correspondiente, por ejemplo para portugués en ./locale/pt/LL_MESSAGES/:

```
cifra-descifra/
├─ README.md
├─ cifradescifra.py
├─ ...
├─ locale/
│  ├─ pt/    
│  │   └─ LL_MESSAGES/
│  │        ├─programa.mo
│  │        └─programa.po
│  ├─ ...
|
├─ ...  
```
El idioma de la aplicación se fija en el archivo .env:
```
IDIOMA = 'es'
```
Nota: Las traducciones para inglés necesitan ser compiladas, lo mismo las cadenas de argparse de español (argparse tiene cadenas exclusivamente en inglés, algunas se han traducido en esta aplicación), en el repositorio están los archivos «po», falta generar los «mo» con «poedit».

[EN] You can use as a base ./locale/program.po and with "poedit" you fill in the translations and compile it to generate the "program.mo" file.  Both files are placed inside the corresponding folder, for example for Portuguese in ./locale/pt/LL_MESSAGES/:
```
cifra-descifra/
├─ README.md
├─ cifradescifra.py
├─ ...
├─ locale/
│  ├─ pt/    
│  │   └─ LL_MESSAGES/
│  │        ├─programa.mo
│  │        └─programa.po
│  ├─ ...
|
├─ ...  
```
The application language is set in the .env file:
```
IDIOMA = 'en'
```
Note: The English translations need to be compiled, the Spanish argparse strings need to be compiled, the po files are in the repository, the mo files need to be generated with "poedit".

# Líneas futuras

1) Intercambio de claves para permitir compartir archivos 
2) Listado de los archivos cifrados 
3) Aplicación móvil
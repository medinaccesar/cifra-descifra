# cifra-descifra
Permite cifrar y descifrar archivos, puede ejecutarse en modo consola, en modo guiado o en modo gráfico. Por defecto en español pero admite otros idiomas.
El cifrado se hace con una clave única, (para cada archivo), que se genera para cada operación de cifrado, estas claves se gestionan internamente y están a su vez cifradas con una clave maestra configurable.

# Requisitos
 Si se quiere usar la interfaz gráfica «tkinter».    
 En linux con apt-get o el gestor de paquetes correspondiente, por ejemplo:
```
 sudo apt-get install python3-tk
 ```
En «windows» está incluido a partir de python 3.

# Instalación de dependencias
Se instalan las dependencias establecidas en el setup:
```
 pip install .    
```
Se compilan los archivos de idiomas:
```
python compile_lang.py 
```
# Uso
```
Uso: cifradescifra.py [-h] [-c ARCHIVO ARCHIVO_CIFRADO | -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO | -g | -a] [--version]

Cifradescifra 1.0.0

argumentos opcionales:
  -h, --help            muestra este mensaje de ayuda y sale
  -c ARCHIVO ARCHIVO_CIFRADO, --cifrar ARCHIVO ARCHIVO_CIFRADO  Cifra el archivo                      
  -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO, --descifrar ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO Descifra el archivo                     
  -g, --gui             Se ejecuta el entorno gráfico
  -a, --asistido        Se ejecuta el modo guiado
  -b, --copiar          Hace una copia de la base de datos
  -r ARCHIVO_COPIA, --restaurar ARCHIVO_COPIA      Restaura una copia de la base de datos
  --version             Muestra la versión del programa
```
# Traducciones / Translations
Se puede usar como base ./locale/programa.po y con «poedit» u otro editor rellenar las traducciones.  El archivo se coloca dentro de la carpeta correspondiente, por ejemplo para portugués en ./locale/pt/LL_MESSAGES/:

```
cifra-descifra/
├─ README.md
├─ cifradescifra.py
├─ ...
├─ locale/
│  ├─ pt/    
│  │   └─ LL_MESSAGES/
│  │        └─programa.po
│  ├─ ...
|
├─ ...  
```
Posteriormente se compila el archivo de traducción ejecutando:
```
python compile_lang.py 
```
El idioma de la aplicación se fija en el archivo .env:
```
IDIOMA = 'es'
```

[EN] You can use as a base ./locale/programa.po and with "poedit" or another editor fill in the translations.  The file is placed inside the corresponding folder, for example for Portuguese in ./locale/pt/LL_MESSAGES/:
```
cifra-descifra/
├─ README.md
├─ cifradescifra.py
├─ ...
├─ locale/
│  ├─ pt/    
│  │   └─ LL_MESSAGES/
│  │        └─programa.po
│  ├─ ...
|
├─ ...  
```
Subsequently, the translation file is compiled by executing:
```
python compile_lang.py 
```
The application language is set in the .env file:
```
IDIOMA = 'en'
```

# Líneas futuras

1) Intercambio de claves para permitir compartir archivos 
2) Listado de los archivos cifrados 
3) Aplicación móvil

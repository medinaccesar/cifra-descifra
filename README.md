
![Static Badge](https://img.shields.io/badge/status-En%20desarrollo-brightgreen)
# cifra-descifra v2.0.0 

Permite cifrar y descifrar archivos, puede ejecutarse en modo consola, en modo guiado o en modo gráfico. Por defecto está en español pero admite otros idiomas.
El cifrado se hace con una clave única que se genera para cada operación de cifrado, estas claves se gestionan internamente y están, a su vez, cifradas con una clave derivada de una clave maestra configurable.

Novedades de la versión 2:

1) Permite elegir el tipo de cifrado:
    1) AES128_CBC
    2) AES256_GCM
    3) XChaCha20_Poly1305 (Más lento en las pruebas)

    Se establece uno por defecto, opción -t.

    Por otra parte se utiliza un cifrado de doble capa de cada una de las claves que se generan en cada operación de cifrado, primero se cifran con AES_GCM y el resultado con AES128_CBC.  

2) Se puede establecer una contraseña de inicio en la aplicación.

3) Permite generar  un fichero para poder compartir un archivo cifrado con otros usuarios, para ello se hace uso del cifrado asimétrico con llave pública y privada. Se podrán importar las llaves públicas de otros usuarios para poder generar estos ficheros en los que se cifrará la clave, (con la que se cifra el archivo),  con la clave pública de cada uno de los usuarios a los que se pretenda compartir, de esta forma  otros usuarios podrán importarlo, descifrarlo con su clave privada, alimentar su aplicación y en definitiva descifrar el archivo.

4) Mejora de la interfaz gráfica (Por hacer)



Nota*: Nueva versión ![2.0.0](https://github.com/medinaccesar/cifra-descifra) ![Static Badge](https://img.shields.io/badge/status-En%20desarrollo-brightgreen)

# Requisitos
 Python 3.
 
 Si se quiere usar la interfaz gráfica se requiere «tkinter».    
 En linux se puede instalar con apt-get o el gestor de paquetes correspondiente, por ejemplo:
```
 sudo apt-get install python3-tk
 ```
En «windows» está incluido a partir de python 3.

# Instalación de dependencias
Se instalan las dependencias :
```
pip install -r requirements.txt 
```
Se compilan los archivos de idiomas:
```
python compile_lang.py 
```
# Uso
```
Uso: cifradescifra.py [-h]
                      [-c ARCHIVO ARCHIVO_CIFRADO | -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO | -g
                      | -a | -b | -r ARCHIVO_COPIA | -C | -Q | -t | -E NOMBRE_ARCHVO
                      | -cc ARCHIVO [CORREO_1, CORREO_2 ...]
                      | -ic ARCHIVO_CLAVE | -l | -i] [--version]


Cifradescifra 2.0.0

argumentos opcionales:
  -h, --help            muestra este mensaje de ayuda y sale
  -c ARCHIVO ARCHIVO_CIFRADO, --cifrar ARCHIVO ARCHIVO_CIFRADO
                        Cifrar archivo
  -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO, --descifrar ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO  Descifrar archivo
  -g, --gui             Se ejecuta el entorno gráfico
  -a, --asistido        Se ejecuta el modo guiado
  -b, --copiar          Hace una copia de la base de datos
  -r ARCHIVO_COPIA, --restaurar ARCHIVO_COPIA
                        Restaura una copia de la base de datos
  -C, --clave           Establece una contraseña para ejecutar el programa
  -Q, --quitar-clave    Desestablece la contraseña
  -t, --tipo-cifrado    Selecciona el tipo de cifrado por defecto
  -E NOMBRE_ARCHIVO, --exportar-clave NOMBRE_ARCHIVO          Exporta tu clave pública
  -cc ARCHIVO [CORREO_1, CORREO_2 ...], --compartir ARCHIVO [CORREO_1, CORREO_2 ...]  Cifrar archivo para compartirlo
  -ic ARCHIVO_CLAVE, --importar-clave ARCHIVO_CLAVE           Importa una clave pública de otro usuario
  -l, --listar-claves   Lista los correos de las claves públicas
  -i, --info            Muesta las opciones establecidas
  --version             Muestra la versión del programa
```
Por ejemplo:

* **Cifrar un archivo en modo consola:**
```
## Cifrar un archivo en modo consola
python cifradescifra.py -c archivo.pdf archivo.pdf.cifrado
Se ejecuta en modo consola
Progreso |████████████████████████████████████████| 100% Completo
El archivo se ha cifrado correctamente.

## Descifrar un archivo en modo consola
python cifradescifra.py -d archivo.pdf.cifrado archivo.pdf
Se ejecuta en modo consola
Progreso |████████████████████████████████████████| 100% Completo
El archivo se ha descifrado correctamente.

## Cifrar o descifrar un archivo en modo gáfico 
python cifradescifra.py -g

## Establecer el tipo de cifrado por defecto
python cifradescifra.py -t
Se ejecuta en modo consola. 

¿Elija el tipo de cifrado? (AES128_CBC/AES256_GCM/XChaCha20_Poly1305) o (c/g/x): g

```
* **Descifrar un archivo en modo consola:**
``` 
python cifradescifra.py -d archivo.pdf.cifrado archivo.pdf
Se ejecuta en modo consola
Progreso |████████████████████████████████████████| 100% Completo
El archivo se ha descifrado correctamente.
``` 
* **Cifrar o descifrar un archivo en modo gráfico:** 
``` 
python cifradescifra.py -g
``` 
* **Cifrar o descifrar un archivo en modo asistido:** 
``` 
python cifradescifra.py -a
``` 
* **Hacer una copia de seguridad de la base con las claves cifradas:**
``` 
python cifradescifra.py -b
```
    Se recomienda de vez en cuando por seguridad para no perder las claves, 
    sin ellas es  imposible descifrar los archivos, o simplemente para importarlas 
    en otro equipo. El archivo se genera en la carpeta ./data/backup/ con el nombre 
    seguido de la fecha y hora en que se generó.

* **Importar una copia de seguridad de la base con las claves cifradas:**
``` 
python cifradescifra.py -r database_230723_125148.db
```
    La importación sustituirá la base de datos actual si la hubiera. 
    Otra forma de restaurarlo es copiando el archivo en la carpera ./data 
    y renombrarlo como database.db

* **Establecer una contraseña  para entrar en la aplicación:**
``` 
python cifradescifra.py -C
Se ejecuta en modo consola. 

Se establecerá una contraseña de inicio 

Intoduzca la contraseña: ****
Repita la contraseña: ****
La contraseña se ha establecido correctamente.
``` 
* **Desestablecer la contraseña de inicio:**
``` 
Intoduzca la contraseña: ****
Se ejecuta en modo consola. 

Se desestablecerá la contraseña de inicio 

Para desestablecerla intoduzca antes la contraseña: ****
La contraseña se ha desestablecido correctamente. 
``` 
* **Establecer el tipo de cifrado por defecto:**
``` 
python cifradescifra.py -t
Se ejecuta en modo consola. 

¿Elija el tipo de cifrado? (AES128_CBC/AES256_GCM/XChaCha20_Poly1305) o (c/g/x): g
``` 
* **Información sobre las opciones establecidas:**
``` 
python cifradescifra.py -i
Se ejecuta en modo consola. 

Opciones establecidas: 

IDIOMA:  es
TIPO_CIFRADO:  AES256_GCM
Requiere clave:  No 

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
IDIOMA = 'pt'
```

# Líneas futuras

1) Interfaz gráfica
2) Aplicación móvil
3) Explorar compartir las claves públicas en una cadena de bloques


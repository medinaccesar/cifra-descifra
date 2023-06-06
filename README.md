# cifra-descifra
Permite cifrar y descifrar archivos, puede ejecutarse en modo consola, en modo guiado o en modo gráfico. Por defecto en español pero admite otros idiomas.
El cifrado se hace con una clave única, (para cada archivo), que se genera en cada operación de cifrado, estas caves se gestionan internamente y están a su vez cifradas con una clave maestra configurable.

# Requisitos
 Para las variables de entorno «python-dotenv», y si se quiere usar la interfaz gráfica «tkinter».        

# Uso
```
Uso: cifradescifra.py [-h] [-c ARCHIVO ARCHIVO_CIFRADO | -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO | -g | -a] [--version]

Cifradescifra 1.0.0

argumentos opcionales:
  -h, --help            muestra este mensaje de ayuda y sale
  -c ARCHIVO ARCHIVO_CIFRADO, --cifrar ARCHIVO ARCHIVO_CIFRADO                        
  -d ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO, --descifrar ARCHIVO_CIFRADO ARCHIVO_DESCIFRADO                        
  -g, --gui             Se ejecuta el entorno gráfico
  -a, --asesorado       Se ejecuta el modo guiado
  --version             Muestra la versión del programa
```

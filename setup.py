from setuptools import setup
from constantes import Configuracion as conf

setup(
    name = conf.NOMBRE_AP,
    version = conf.VERSION,
    packages = [''],
    install_requires=[
        'python-dotenv',
        'python-gettext',
        'cryptography',                
        'chacha20poly1305'
        # 'pandas',
        # 'SQLAlchemy'             
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: GNU GENERAL PUBLIC LICENSE V3',
        'Operating System :: OS Independent',
    ],
    description=conf.DESCRIPCION_APP,
    url='https://github.com/medinaccesar/cifra-descifra'
)

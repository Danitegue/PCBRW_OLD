#!/usr/env/python
# -*- coding: iso-8859-15 -*-

# ------------------------------------------------------------------------
# <?xml version='1.0' encoding='iso-8859-15'?>
# <module>
#   <header>
#     <name>log</name>
#     <type>module</type>
#     <author>EDUCACION\jrodrosu</author>
#     <desc>
#       Biblioteca de funciones que implementa la clase log_sistemas. Esta
#       clase permite a los programas crear un fichero de log (incluso en el
#       eventlog de windows). Los logs siguen el formato "estandar" de
#       Unix/linux.
#     </desc>
#   </header>
# ------------------------------------------------------------------------

import logging, logging.handlers


# Importamos los niveles desde logging, para no tener que poner log.logging.NIVEL
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


# ------------------------------------------------------------------------
# <object>
#   <name>log_sistemas</name>
#   <type>class</type>
#   <author>
#     <username>EDUCACION\jrodrosu</username>
#   </author>
#   <desc>
#     log_sistemas(sFileName, sLogID, sFormat = None, bAppend = True,
#     iMaxSize = 0, iBackupCount = 5) Clase que crea un objeto de logger.
#     Se inicializa con el nombre del archivo. Por defecto, se añade al
#     final del archivo (bAppend = True), pero se puede especificar que se
#     cree otro log. Si sFileName es '', se usa la consola de pantalla. *
#     sLogID es el nombre de la instancia del Log. Debe de ser única dentro
#     de un mismo proceso (ojo con los threads). Es una cadena
#     identificativa que aparecerá en el log, en cada línea (generalmente
#     es el nombre de la aplicación). * sFormat (opcional) es una cadena
#     que especifica el formato de salida del log. Por defecto es
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s". El
#     parámetro opcional iMaxSize especifica el tamaño máximo del
#     archivo. Cuando se alcance, se rotará el log (se le añadirá una
#     extensión numérica y se creará otro fichero .log). Si se
#     especifica 0, el log nunca se rotará (este es el caso por
#     defecto). * iBackupCount indica cuantas copias de seguridad
#     (rotacion del log) se hacen antes de que empiecen a borrarse las más
#     antiguas. Por defecto vale 5 (se quedan las 5 más recientes). Es
#     recomendable que el fichero tenga extensión .log
#   </desc>
# </object>
# ------------------------------------------------------------------------
class log_sistemas:
    def __init__(self, sFileName, sLogID, sFormat = None, bAppend = True, iMaxSize = 0, iBackupCount = 5):
        '''Constructor que se inicializa con el nombre del archivo. Por defecto,
        se añade al final del archivo (bAppend = True), pero se puede especificar que
        se cree otro log. Si sFileName es '', se usa la consola de pantalla.

        sLogID es el nombre de la instancia del Log. Debe de ser única dentro de
        un mismo proceso (ojo con los threads). Es una cadena identificativa que
        aparecerá en el log, en cada línea (generalmente es el nombre de la aplicación).

        sFormat (opcional) es una cadena que especifica el formato de salida del log. Por
        defecto es "%(asctime)s - %(name)s - %(levelname)s - %(message)s".

        El parámetro opcional iMaxSize especifica el tamaño máximo del archivo. Cuando
        se alcance, se rotará el log (se le añadirá una extensión numérica y se creará
        otro fichero .log). Si se especifica 0, el log nunca se rotará (este es el caso
        por defecto).

        iBackupCount indica cuantas copias de seguridad (rotacion del log) se hacen antes
        de que empiecen a borrarse las más antiguas. Por defecto vale 5 (se quedan las 5
        más recientes).

        Es recomendable que el fichero tenga extensión .log'''

        self.sFileName = sFileName
        self.logger = logging.getLogger(sLogID)
        self.logger.setLevel(logging.INFO)

        #crea fichero de log handler y establece level to INFO        
        if sFileName == '':
            fh = logging.StreamHandler()
        else:        
            fh = logging.handlers.RotatingFileHandler(sFileName, maxBytes = iMaxSize, backupCount = iBackupCount)
            
        fh.setLevel(logging.INFO)
        
        if not bAppend: # Si no se añade al final, creamos un backup y empezamos de cero.
            fh.doRollover()

        if sFormat is None: # Si no se especificó formato (o se puso None), ponemos uno por defecto.
            sFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            
        formatter = logging.Formatter(sFormat)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # Los siguientes métodos se definen porque no se ha heredado directamente de
    # la clase log

    def info(self, sText):
        self.logger.info(sText)

    def warning(self, sText):
        self.logger.warning(sText)

    def debug(self, sText):
        self.logger.debug(sText)

    def error(self, sText):
        self.logger.error(sText)

    def error(self, sText):
        self.logger.critical(sText)

    def log(self, level, sText):
        self.logger.log(level, sText)


# ------------------------------------------------------------------------
# </module>
# ------------------------------------------------------------------------
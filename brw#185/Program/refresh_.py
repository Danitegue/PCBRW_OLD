#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#

'''
refresh.py

Use mode: refresh.py [options]
  -h,--help			Shows this help
  -i,--input=		File to process. If the given file is a directory, all files within will be processed.
  -s,--servers=		Comma separated list of xmlrpc server nicks (defined in .ini config file)
  -b,--brewerid=	Brewerid of file/s to process

Ej:
  refresh.py -b 033 -s iberonesia -i brewernet\datos

'''

import sys
import xmlrpclib
import zipfile
import os
import tempfile
import md5
import datetime
import re

import log

from optparse import OptionParser
from refreshdb import RefreshDbInfo
from refreshdb import DBMRefreshDb
from refreshdb import CSVRefreshDb
from xmlrpcproxy import ProxiedTransport

import util
from util import IniParser
from util import Options
from util import ServerDef
from util import IniException
from util import ParamException
from util import ArraySplitter

import socket

RefreshDbImpl = CSVRefreshDb  # Si se quiere usar CSV
# RefreshDbImpl = DBMRefreshDb  # Si se quiere usar DBM

FILELIST_STEP=200				# Número máximo de ficheros a pedir por cada petición de listado al servidor.
FILETRANSFER_STEP=524288		# Umbral en KB para enviar un grupo de ficheros.


# Global flags (configured from the command line or the .ini file)
VERBOSITY_LEVEL = log.ERROR
LOGGER = None


def report(msg, loglevel = log.INFO):
	''' Saca un error por pantalla y por el log.
	'''
	if loglevel >= VERBOSITY_LEVEL: print msg

	if LOGGER is not None:
		LOGGER.log(loglevel, msg)

	

class Refresh:

	def __init__(self, brewerid, server_def, fullfilenames):
		'''
		Refresca los ficheros generados por el brewer en el servidor.

		brewerid: brewerid de los ficheros
		server_def : contiene las definiciones del servidor: url y ruta hacia la base de datos de refresh.
		fullfilenames : lista de rutas absolutas de los ficheros a enviar.
		'''
		if server_def.proxy is None:
			self.server = xmlrpclib.Server(server_def.url + '/xmlrpc/')
		else:
			self.server = xmlrpclib.Server(server_def.url + '/xmlrpc/', transport = ProxiedTransport(server_def.proxy))
			
		self.brewerid = brewerid
		self.fullfilenames = fullfilenames
		self.dbfile_path = server_def.dbfile

		# Statistics
		self.available = len(fullfilenames)
		self.sent = 0
		self.failed = 0

		#self.log = True

		self.debug("Starting refresh from", brewerid, "to", server_def.url)
		self.debug("Files to process:", fullfilenames)


	def debug(self, *args):
		report(' '.join([str(x) for x in args]), log.INFO)


	def refreshFiles(self):
		'''
		Realiza el procesamiento de los ficheros que contiene fullfilenames.
		Se determina si se deben enviar o no y se envían comprimidos los que sí.
		Se actualiza la base de datos refresh con los ficheros enviados correctamente.
		'''

		#
		# Si la refreshdb no existe, la regeneramos a partir de la información del servidor.
		#
		if not os.path.exists(self.dbfile_path):
			self.debug("Regenerating refreshdb...")
			self.regenerateRefreshDb(self.fullfilenames, self.dbfile_path)

		if self.fullfilenames == []:
			report('No files to send. Nothing done.', log.WARN)
			return

		db = RefreshDbImpl(None, self.dbfile_path)
		db.open()
		files_to_send = []			### Lista de RefreshDbInfo de los ficheros a enviar.
		size_to_send = 0

		for fullfilename in self.fullfilenames:
			filename = os.path.basename(fullfilename)

			db_info = db.read(filename)
			file_info = self.infoFromFilename(fullfilename)

			if not self.needSend(db_info, file_info):
				continue
			
			files_to_send.append(file_info)
			size_to_send += file_info.size

			if size_to_send > FILETRANSFER_STEP:
				self.debug("Sending files:", [ os.path.basename(info.filename) for info in files_to_send ], "  Total size =", size_to_send)
				self.sendFilesAndUpdate(db, files_to_send)
				files_to_send = []
				size_to_send = 0
			
		if files_to_send != []:
			self.debug("Sending files:", [ os.path.basename(info.filename) for info in files_to_send ], "  Total size =", size_to_send)
			self.sendFilesAndUpdate(db, files_to_send)
		db.close()

		title = "Brewer%03d -> %s" % (self.brewerid, self.server._ServerProxy__host)

		print
		print title
		print "-" * len(title)
		print "Files available: %d" % ( self.available )
		print "Files sent: %d" % ( self.sent )
		print "Failed: %d" % ( self.failed )


	def queryFiles(self):
		return self.queryFilesImpl(self.fullfilenames)


	def queryFilesImpl(self, fullfilenames):
		'''
		Obtiene la información que contiene el servidor sobre los ficheros dados.
		Devuelve un diccionario con clave el nombre de fichero y valor el RefreshDbInfo asociado.
		'''
		#
		# Hacemos un listado escalonado. Demasiados ficheros provocan un timeout.
		#
		result = {}
		splitter = ArraySplitter(fullfilenames, FILELIST_STEP)
		for group in splitter:
			# al volver de la funcion, result se ha actualizado.
			self.queryFilesPart(result, group)

		return result

		
	def queryFilesPart(self, infomap, fullfilenames):
		'''
		Obtiene la informacion que tiene el servidor sobre una lista de ficheros.
		Efectua la llamada al servidor y actualiza el diccionario que se pasa como parametro con la informaicion.
		Parametros:
			infomap       : diccionario a rellenar con la informacion del servidor. Clave: nombre de fichero; Valor: RefreshDbInfo asociado.
			fullfilenames : lista de rutas completas de los ficheros a consultar.
		'''
		filenames = [ os.path.basename(f) for f in fullfilenames ]
		self.debug("Retrieving info about:", filenames)

		#
		# El resultado es un dict con claves y valores:
		# size : tamaño del fichero.
		# md5sum : md5sum del fichero.
		# datetime : fecha hora del archivo
		#
		try:
			maplist = self.server.receive_filelist(self.brewerid, filenames)
		except socket.gaierror:
			report("ERROR: Could not connect to server. Exiting...")
			sys.exit(1)

		for (fname, map) in maplist.iteritems():
			if map is False:
				continue
			#
			# Construimos el DbRefreshInfo
			# En python2.5 ya hay un parser para fechas.
			#
			dt_parts = map['datetime'].split(" ")
			date_parts = [ int(part) for part in dt_parts[0].split("-") ]
			time_parts = [ int(part) for part in dt_parts[1].split(":") ]
			dt = datetime.datetime(date_parts[0], date_parts[1], date_parts[2], time_parts[0], time_parts[1], time_parts[2])
			remote_info = RefreshDbInfo(map['filename'], dt, map['size'], map['md5sum']) 
			infomap[map['filename']] = remote_info
			
		return
		

	def regenerateRefreshDb(self, fullfilenames, dbfile_path):
		'''
		Regenera la base de datos local de refresco.
		Pregunta al servidor por la informacion de los ficheros y crea una nueva base de datos.

		Parametros:
			fullfilenames: rutas completas de los ficheros a consultar.
			dbfile_path  : ruta completa a la base de datos a generar.
		'''
		files_info = self.queryFilesImpl(fullfilenames)
		db = RefreshDbImpl(None, dbfile_path)
		db.open()
		for info in files_info.itervalues():
			db.write(info.filename, info)
		db.close()


	def infoFromFilename(self, fullfilename):
		'''
		Construye una instancia RefreshDbInfo a partir de la ruta de un fichero.
		NOTA: info.filename es la ruta ABSOLUTA del fichero.
		'''
		size = os.path.getsize(fullfilename)
		dt = datetime.datetime.fromtimestamp(os.path.getmtime(fullfilename))
		md5sum = md5.new(open(fullfilename, 'rb').read()).hexdigest()
		info = RefreshDbInfo(fullfilename, dt, size, md5sum)
		return info
		

	def needSend(self, db_info, file_info):
		'''
		Determina si un fichero debe ser o no enviado al servidor verificando si ha
		cambiado respecto a la versión existente en el servidor.

		db_info: información del fichero en la base de datos refresh. Es una instancia RefreshDbInfo
		file_info: información del fichero en el sistema de ficheros. Es una instancia RefreshDbInfo
		'''
		to_compare = db_info

		if to_compare is None:
			return True

		# Si los ficheros en contenido son iguales, da igual que la fecha sea diferente.
		if (to_compare.datetime != file_info.datetime or 
				(to_compare.md5sum != file_info.md5sum and to_compare.size != file_info.size) ):
			return True

		return False

	
	def sendFilesAndUpdate(self, db, files_to_send):
		'''
		Envía un conjunto de ficheros y actualiza los datos en la refreshdb.

		files_to_send: lista de DBRefreshInfo de los ficheros a enviar.
		'''
		md5sums = self.sendFiles(files_to_send)
		self.checkAndUpdateRefreshDb(db, md5sums, files_to_send)
		self.sent += len(files_to_send)


	def sendFiles(self, files_to_send):
		'''
		files_to_send: lista de DBRefreshInfo de los ficheros a enviar.

		Envía un conjunto de ficheros al servidor.
		Los ficheros se envían dentro de un archivo comprimido.

		NOTA: info.filename debe ser la ruta ABSOLUTA del fichero.
		'''

		fnames = []
		zip_fname = tempfile.mktemp()

		report("Creating tmp file: '%s'" % zip_fname, log.DEBUG)

		zip_file = zipfile.ZipFile(zip_fname, 'w')
		for info in files_to_send:
			fullfilename = info.filename
			filename = os.path.basename(fullfilename)
			fnames.append(filename)
			report("Adding file '%s' to zipfile." % filename, log.INFO)
			zip_file.write(fullfilename, filename)

		zip_file.close()

		data = xmlrpclib.Binary(open(zip_fname, "rb").read())
		result = self.server.receive_files(self.brewerid, data)

		report("Deleting tmp file: '%s'" % zip_fname, log.DEBUG)
		os.unlink(zip_fname)

		return result


	def checkAndUpdateRefreshDb(self, db, md5sums, files_sent):
		'''
		Comprueba que el fichero fue enviado correctamente, actualizando la refreshdb en tal caso.
		db: Base de datos Refresh.
		md5sums: lista de md5sums recibidos por el servidor.
		files_sent: lista de RefreshDbInfo de los ficheros enviados. 

		Si el md5sum recibido es igual al que se obtuvo del fichero, éste fue enviado correctamente.
		Si ocurriera que el fichero fue modificado tras tomar el info, en la siguiente ejecución 
		se detectará el cambio y se reenviará.
		'''
		for (md5sum, info) in zip(md5sums, files_sent):
			if (md5sum == info.md5sum):
				filename = os.path.basename(info.filename)		### Nos aseguramos que usamos el basename
				db.write(filename, info)
			else:
				self.debug("Failed transfer for:", info.filename)
				self.failed += 1

		#
		# Nos aseguramos de que se escriben los datos.
		#
		db.flush()


def usage(argv):
	 print __doc__


class OptionBuilder(object):
	'''
	Construye un objeto que contiene las opciones definidas en el fichero de configuración 
	y en los parámetros pasados al programa por línea de comandos.

	Las opciones definidas en el archivo de configuración son sobreescritas por las definidas como parámetro.
	Si alguna opción es necesaria y no se encuentra especificada, se lanza una ParamException.

	Si alguna opción especificable solamente mediante el fichero de configuración no está definida, se lanza
	una IniException.
	'''
	
	def __init__(self, ini_filename):
		'''
		ini_filename : Nombre por defecto del fichero .ini
		'''
		
		self.iniParser = IniParser(ini_filename)
		self.options = None

		self.servers_str = self.iniParser.servers_str
		self.brewerid_str = self.iniParser.brewerid_str
		self.input_str = self.iniParser.input_str
		self.rundir_str = self.iniParser.rundir_str
		self.config_str = "config"

	#
	# Propiedades
	#
	def getServerDefs(self):
		return self.iniParser.server_defs

	server_defs = property(getServerDefs)

	def getOptions(self):
		'''
		Construye el objeto de opciones, analizando tanto el fichero de configuración como los parámetros.
		'''
		#
		# Leemos primero los parámetros para poder contemplar el especificar un fichero de configuración diferente.
		#
		global VERBOSITY_LEVEL 

		(paramOptions, paramArgs) = self.parseArgs()
		if paramOptions.config != None:
			self.iniParser.ini_path = paramOptions.config

		self.iniParser.parseIni()
		self.options = self.iniParser.options
		VERBOSITY_LEVEL = log.ERROR - 10 * paramOptions.verbosity

		if paramOptions.brewerid is not None:
			self.options.brewerid = paramOptions.brewerid
		if paramOptions.servers is not None:
			self.options.servers = paramOptions.servers
		if paramOptions.input is not None:
			self.options.input = paramOptions.input

		#
		# Comprobamos las opciones mínimas.
		#
		if self.options.servers is None:
			raise ParamException("-s must be specified")
		if self.options.brewerid is None:
			raise ParamException("-b must be specified")
		if self.options.input is None:
			raise ParamException("-i must be specified")
		if self.options.rundir is None:
			raise IniException("'working_dir' option must be specified in .ini file")

		util.check_input(self.options.input)
		self.options.brewerid = util.check_brewerid(self.options.brewerid)



	def parseArgs(self):
		self.parser = OptionParser()
		parser = self.parser
		parser.add_option("-" + self.input_str[0], "--" + self.input_str, dest=self.input_str, 
				help="File to process. If the given file is a directory, all files within will be processed.", metavar="FILE")
		parser.add_option("-" + self.servers_str[0], "--" + self.servers_str, dest=self.servers_str, 
				help="Comma separated list of xmlrpc server aliases")
		parser.add_option("-" + self.brewerid_str[0], "--" + self.brewerid_str, dest=self.brewerid_str, 
				help="Brewerid of file/s to process")
		parser.add_option("-" + self.config_str[0], "--" + self.config_str, dest=self.config_str, 
				help="Configuration file path", metavar="FILE")
		parser.add_option("-v", "--verbose", dest='verbosity', default=0, action="count", 
				help="Verbosity level. The more '-v' the more verbose is the program.")

		return parser.parse_args()


	def printHelp(self):
		self.parser.print_help()



def applyFilter(brewerid, fullfilenames):
	#
	# Esto podría ser más eficiente...
	#
	pattern = re.compile(r".*\.%03d$" % brewerid)
	result = []
	for f in fullfilenames:
		if pattern.match(f):
			result.append(f)
	return result


def main(argv):
	try:
		optionbuilder = OptionBuilder('client.ini')
		optionbuilder.getOptions()

		options = optionbuilder.options
		server_defs = optionbuilder.server_defs

		if os.path.isfile(options.input):
			fullfilenames = [ options.input ]
		else:
			fullfilenames = util.files_in_dir(options.input)

		fullfilenames = applyFilter(options.brewerid, fullfilenames)
		servers = options.servers.split(',')

		for server in servers:
			try:
				server_def = server_defs[server]
			except KeyError:
				raise ParamException("Invalid server: " + server)
			refresh = Refresh(options.brewerid, server_def, fullfilenames)
			refresh.refreshFiles()

	except ParamException, e:
		print "Error:", e
		optionbuilder.printHelp()
		sys.exit(2)

	except IniException, e:
		print "Error in .ini file:", e
		sys.exit(2)
	

if __name__ == "__main__":
	main(sys.argv[1:])


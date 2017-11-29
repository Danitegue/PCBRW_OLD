#
# -*- coding: iso-8859-15 -*-
#

import ConfigParser
import os
from urllib import unquote, splittype, splithost


class ArraySplitter:
	'''
	Iterator que parte un array en trozos de una longitud determinada.
	'''
	def __init__(self, array, step):
		self.array = array
		self.step = step
		self.pos = 0

	def __iter__(self):
		return self

	def next(self):
		if self.pos >= len(self.array):
			raise StopIteration

		result = self.array[self.pos : self.pos + self.step]
		self.pos += self.step

		return result


def check_filename(filename):
	if not os.path.isfile(filename):
		raise ParamException("'" + filename + "' is not a regular file")

def check_dirname(dirname):
	if not os.path.isdir(dirname):
		raise ParamException("'" + dirname + "' is not a directory")

def check_input(filename):
	if not os.path.isdir(filename) and not os.path.isfile(filename):
		raise ParamException("'" + filename + "' is neither a directory nor a file")

def check_brewerid(brewerid):
	try:
		return int(brewerid)
	except ValueError:
		raise ParamException("'" + brewerid + "' is not a valid brewer id")

def files_in_dir(dirname):
 
	result = [ os.path.join(dirname, fname) for fname in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, fname) ) ]
	return result

class IniException(Exception):
	pass

class IniFileNotExist(IniException):
	pass

class ParamException(Exception):
	pass

class ServerDef:
	'''
	Contiene la descripción de una sección de servidor en el fichero de configuración
	'''
	def __init__(self, url, dbfile, proxy = None):
		self.url = url
		self.dbfile = dbfile
		self.proxy = proxy

class Options:
	def __init__(self):
		self.brewerid = None
		self.servers = None
		self.input = None
		self.rundir = None

class IniParser:
	'''
	Construye el objeto de opciones leídas del fichero de configuración.

	Modo de uso:
	iniparser = IniParser('client.ini')
	iniparser.ini_path = '/tmp/clientconfiguration.ini'
	iniparser.parseIni()

	options = iniparser.options
	server_defs = iniparser.server_defs
	'''
	def __init__(self, ini_filename):
		self.ini_filename = ini_filename
		self.ini_path = None		# Si se modifica, se intenta leer el fichero de configuración del nombre de fichero definido por ini_path.
		self.options = Options()
		self.server_defs = {}		# Diccionario de ServerSection. Clave: url del servidor. Valor: ServerSection.
		self.proxy = None
	
		self.globalSection_str = 'global'
		self.servers_str = 'servers'
		self.brewerid_str = 'brewerid'
		self.input_str = 'input'
		self.rundir_str = 'working_dir'
		self.proxy_str = 'proxy'
		self.noproxy_str = 'noproxy'


	def parseIni(self):
		ini_filename = self.ini_filename
		if not os.path.exists(ini_filename):
			raise IniFileNotExist('File "%s" does not exists.' % ini_filename)

		if not os.path.isfile(ini_filename):
			raise IniException('"%s" is not a file.' % ini_filename)	

		global_str = self.globalSection_str

		self.ini = ConfigParser.RawConfigParser()
		home_ini = '~/.%s' % ini_filename
		etc_ini = os.path.join( os.path.sep + 'data', 'etc', '%s' % ini_filename )
		if self.ini_path != None:
			paths = [ self.ini_path ]
		else:
			paths = [ini_filename, os.path.expanduser(home_ini), etc_ini]
		self.ini.read(paths)

		self.options.servers = self.getGlobalOption(self.servers_str)
		self.options.brewerid = self.getGlobalOption(self.brewerid_str)
		self.options.input = self.getGlobalOption(self.input_str)
		self.options.rundir = self.getGlobalOption(self.rundir_str)
		self.proxy = self.getGlobalOption(self.proxy_str)
		self.server_defs = self.parseServers()


	def parseServers(self):
		server_sections = [ section for section in self.ini.sections() if section != self.globalSection_str ]
		result = {}
		for section in server_sections:
			try:
				url = self.ini.get(section, 'url')
			except ConfigParser.NoOptionError:
				raise IniException('url option must be specified for ' + section + ' server')
			try:
				dbfile = self.ini.get(section, 'db')
				#
				# dbfile está en el directorio rundir.
				#
				dbfile = os.path.join(self.options.rundir, dbfile)
			except ConfigParser.NoOptionError:
				raise IniException('db option must be specified for ' + section + ' server')

			#
			# Si noproxy es falso, se copia el valor proxy de la sección global.
			#
			try:
				noproxy = self.ini.get(section, 'noproxy')
				if noproxy == 'yes' or noproxy == '1' or noproxy == 'true':
					proxy = None
				else:
					proxy = self.proxy
			except ConfigParser.NoOptionError:
				proxy = self.proxy

			server_def = ServerDef(url, dbfile, proxy)
			result[section] = server_def
			
		return result


	def getGlobalOption(self, optionName):
		try:
			return self.ini.get(self.globalSection_str, optionName)
		except ConfigParser.NoOptionError:
			return None


def split_proxy_URL(proxy):
	if proxy is None:
		return None, None, None

	try:
		if proxy[:7] != 'http://':  # Ensures proxy string begins with 'http://'
			proxy = 'http://' + proxy
	except:
		pass

	proxy_username = proxy_password = None

	urltype, r_type = splittype(proxy)
	proxy, XXX = splithost(r_type)
	if '@' in proxy:
		proxy_username, proxy = proxy.split('@', 1)
		if ':' in proxy_username:
			proxy_username, proxy_password = proxy_username.split(':', 1)

	return proxy, proxy_username, proxy_password



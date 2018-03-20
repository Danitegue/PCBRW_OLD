#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#

'''
alive.py

Use mode: alive.py [options]
  -h,--help			Shows this help
  -s,--servers=		Comma separated list of xmlrpc server nicks (defined in .ini config file)
  -b,--brewerid=	Brewerid

Ej:
  alive.py -b 033

'''

import sys
import xmlrpclib
import os
from optparse import OptionParser
from xmlrpcproxy import ProxiedTransport
import util
from util import IniParser
from util import Options
from util import ServerDef
from util import IniException


class Pinger:


	def __init__(self, brewerid, server_def):
		'''
		Construye el objeto Pinger

		brewerid: brewerid de los ficheros
		server_def : contiene las definiciones del servidor: url y ruta hacia la base de datos de refresh.
		'''
		if server_def.proxy is None:
			self.server = xmlrpclib.Server(server_def.url + '/xmlrpc/')
		else:
			self.server = xmlrpclib.Server(server_def.url + '/xmlrpc/', transport = ProxiedTransport(server_def.proxy))
			
		self.brewerid = brewerid

		# Estadísticas
		self.sent = 0
		self.failed = 0


	def doPing(self):
		'''
		Envía un ping al servidor.
		'''

		result = self.server.ping(self.brewerid)


def usage(argv):
	 print __doc__


class ParamException(Exception): pass


class OptionBuilder(object):
	
	def __init__(self, ini_filename):
		
		self.iniParser = IniParser(ini_filename)
		self.options = None

		self.servers_str = self.iniParser.servers_str
		self.brewerid_str = self.iniParser.brewerid_str

	#
	# Propiedades
	#
	def getServerDefs(self): return self.iniParser.server_defs
	server_defs = property(getServerDefs)

	def getOptions(self):
		self.iniParser.parseIni()
		self.options = self.iniParser.options
		self.parseArgs()

		if self.options.servers is None:
			raise ParamException("-s must be specified")
		if self.options.brewerid is None:
			raise ParamException("-b must be specified")
		self.options.brewerid = util.check_brewerid(self.options.brewerid)


	def parseArgs(self):
		self.parser = OptionParser()
		parser = self.parser
		parser.add_option("-" + self.servers_str[0], "--" + self.servers_str, dest=self.servers_str, 
				help="Comma separated list of xmlrpc server nicks")
		parser.add_option("-" + self.brewerid_str[0], "--" + self.brewerid_str, dest=self.brewerid_str, 
				help="Brewerid")

		(options, args) = parser.parse_args()

		if options.brewerid is not None:
			self.options.brewerid = options.brewerid
		if options.servers is not None:
			self.options.servers = options.servers


	def printHelp(self):
		self.parser.print_help()


def main(argv):

	try:
		optionbuilder = OptionBuilder('client.ini')
		optionbuilder.getOptions()

		options = optionbuilder.options
		server_defs = optionbuilder.server_defs

		servers = options.servers.split(',')

		for server in servers:
			try:
				server_def = server_defs[server]
			except KeyError:
				raise ParamException("Invalid server: " + server)
			pinger = Pinger(options.brewerid, server_def)
			pinger.doPing()

	except ParamException, e:
		print "Error:", e
		optionbuilder.printHelp()
		sys.exit(2)
	except IniException, e:
		print "Error in .ini file:", e
		sys.exit(2)
	

if __name__ == "__main__":
	main(sys.argv[1:])


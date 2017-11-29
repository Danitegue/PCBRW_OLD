#
# -*- coding: iso-8859-15 -*-
#

import datetime
import anydbm
import csv

class RefreshDbInfo:
	'''
	La base de datos RefreshDb utiliza esta clase como parámetro de entrada y salida.
	Contiene la información necesaria para definir el estado de un fichero.
	'''

	def __init__(self, filename = None, datetime  = None, size = None, md5sum = None):
		self.fieldsep = ','
		self.dtsep = ':'
		self.dtformat = '%Y' + self.dtsep + '%m' + self.dtsep + '%d' + self.dtsep + '%H' + self.dtsep + '%M' + self.dtsep + '%S'

		self.filename = filename
		self.datetime = datetime
		self.size = size
		self.md5sum = md5sum

	def __str__(self):
		return "filename = %s, datetime = %s, size = %d, md5sum = %s" % (self.filename, self.datetime, self.size, self.md5sum)

	def __repr(self):
		return "filename = %s, datetime = %s, size = %d, md5sum = %s" % (self.filename, self.datetime, self.size, self.md5sum)

	def serialize(self):
		'''
		Serializa el contenido de la instancia a una cadena, lista para guardarse en la base de datos.
		'''
		if self.datetime is None:
			raise ValueError('datetime cannot be None')
		if self.size is None:
			raise ValueError('size cannot be None')
		if self.md5sum is None:
			raise ValueError('md5sum cannot be None')
		return '%s%s%d%s%s' % (self.datetime.strftime(self.dtformat), self.fieldsep, self.size, self.fieldsep, self.md5sum)

	def deserialize(self, string):
		'''
		Rellena la instancia con el valor de una cadena proveniente de la base de datos (deserialización).
		'''
		values=string.split(self.fieldsep)
		dt = values[0]
		self.size=int(values[1])
		self.md5sum = values[2]

		dt_parts = [ int(i) for i in dt.split(self.dtsep) ]
		self.datetime = datetime.datetime(dt_parts[0], dt_parts[1], dt_parts[2], dt_parts[3], dt_parts[4], dt_parts[5])


class RefreshDb:
	'''
	Contrato que debe cumplir una implementación de una base de datos de refresh.
	'''

	def open():
		'''
		Abre la base de datos. La base de datos a abrir habrá sido especificada previamente.
		'''
		raise NotImplementedError()

	def read(filename):
		'''
		Devuelve un RefreshDbInfo con la información en la base de datos correspondiente a filename.
		Si no existen datos, se devuelve None.
		'''
		raise NotImplementedError()

	def write(filename, info):
		'''
		Modifica en la base de datos la información correspondiente a filename.
		'''
		raise NotImplementedError()

	def close():
		'''
		Se cierra la base de datos. La operación debe asegurarse de que se actualicen los datos modificados
		durante la sesión.
		'''
		raise NotImplementedError()

	def flush():
		'''
		Esta operación asegura que se actualizan los datos modificados sin necesidad de cerrar la base de datos.
		'''
		raise NotImplementedError()

	def delete(filename):
		'''
		Operación opcional. Elimina de la base de datos la información correspondiente a filename
		'''
		raise NotImplementedError()



class DBMRefreshDb(RefreshDb):

	def __init__(self, xmlrpc_server_id, dbfile_path):
		self.server = xmlrpc_server_id
		self.dbfile = dbfile_path

	def open(self):
		self.db = anydbm.open(self.dbfile, 'c') 

	def close(self):
		self.db.close()

	def read(self, filename):
		'''
		filename: nombre de fichero del cual se quiere extraer la información.
		Devuelve: instancia de tipo RefreshDBInfo; None en caso de no existir.
		'''
		value = self.db.get(filename)
		if value == None:
			return None

		#
		# Deserialización
		#
		info = RefreshDbInfo(filename)
		info.deserialize(value)

		return info

	def write(self, filename, info):
		#
		# Serialización
		#
		value = info.serialize()

		self.db[filename] = value

	def flush():
		pass


class CSVRefreshDb(RefreshDb):
	def __init__(self, xmlrpc_server, csvfile_path):
		self.server = xmlrpc_server
		self.csvfile = csvfile_path
		self.data = {}

	def open(self):
		try:
			reader = csv.reader(open(self.csvfile, "rt"), dialect="excel", delimiter = ';')
			for row in reader:
				self.data[row[0]] = row[1:]
		except IOError, v:
			if v.errno != 2: # si no es un "File not found", relanzamos la excepción
				raise v
			open(self.csvfile, 'wt') # Creamos el fichero (y se cierra)
			

	def flush(self):
		writer = csv.writer(open(self.csvfile, "wt"), dialect="excel", delimiter = ';')		
		for row in self.data.keys():
			writer.writerow([row] + self.data[row])

	def close(self):
		self.flush()

	def read(self, filename):
		'''
		filename: nombre de fichero del cual se quiere extraer la información.
		Devuelve: instancia de tipo RefreshDBInfo; None en caso de no existir.
		'''
		try:
			value = self.data[filename]
		except KeyError:
			return None

		#
		# Deserialización
		#
		info = RefreshDbInfo(filename)
		info.deserialize(','.join(value))

		return info

	def write(self, filename, info):
		#
		# Serialización
		#
		value = info.serialize()
		self.data[filename] = value.split(',')



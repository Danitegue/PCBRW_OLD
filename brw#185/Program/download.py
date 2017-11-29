#!/usr/bin/env python
import sys
import xmlrpclib
import zipfile
import os


def download(filename):
	server_url = 'http://www.iberonesia.net:8080/xmlrpc/';
	server = xmlrpclib.Server(server_url);
   
	filedata = server.upload(filename)
	dest_file = open(filename, 'wb')
	dest_file.write(filedata.data)

def main(argv):
	for filename in argv:
		download(filename)

if __name__ == "__main__":
	main(sys.argv[1:])


#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from xmlrpclib import Transport
from xmlrpclib import ProtocolError
from urllib import unquote, splittype, splithost
import base64
import util

class ProxiedTransport(Transport):
	'''
	Connect to server.

	@param host Target host.
	@return A connection handle.
	'''

	def set_proxy(self, proxy):
		''' Parses proxy server string, extracting user and password.
		'''
		self.proxy, self.proxy_username, self.proxy_password = util.split_proxy_URL(proxy)


	def __init__(self, proxy):
		''' Creates a new proxy transport instance.
		The proxy scheme can be in the form [http://]user:passwd@server:port

		E.g. http://administrator:0123pass@proxy.server:8080
		'''
		self.set_proxy(proxy)
		self._use_datetime = True
		self.user_agent = 'Iberonesia-Updater 1.0 Beta'


	def make_connection(self, host):
		''' Create a HTTP connection object from a host descriptor
		'''
		import httplib
		self.realhost = host

		return httplib.HTTP(self.proxy)


	def send_request(self, connection, handler, request_body):
		connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))


	def send_host(self, connection, host):
		connection.putheader('Host', self.realhost)


	def send_auth(self, connection, user, password):
		if user is None or password is None:
			return

		cred = base64.encodestring("%s:%s" % (unquote(user), unquote(password))).strip()
		cred = cred.replace("\012", "")
		connection.putheader("Proxy-authorization", "Basic %s" % cred)


	def parse_response(self, f):
		''' reads response from input file, and parses it
		'''
		p, u = self.getparser()

		while True:
			response = f.read(1024)
			if not response: break
			if self.verbose: print "body:", repr(response)
			p.feed(response)

		f.close()
		p.close()

		return u.close()


	def request(self, host, handler, request_body, verbose = 0):
		'''
		Send a complete request, and parse the response.
		
		 @param host Target host.
		 @param handler Target PRC handler.
		 @param request_body XML-RPC request body.
		 @param verbose Debugging flag.
		 @return XML response.
		'''
		# issue XML-RPC request

		self.verbose = verbose

		h = self.make_connection(host)
		if verbose:
			h.set_debuglevel(1)

		self.send_request(h, handler, request_body)
		self.send_host(h, host)
		self.send_auth(h, self.proxy_username, self.proxy_password)
		self.send_user_agent(h)
		self.send_content(h, request_body)

		errcode, errmsg, headers = h.getreply()

		if errcode != 200:
			raise ProtocolError(host + handler, errcode, errmsg, headers)

		return self.parse_response(h.getfile())



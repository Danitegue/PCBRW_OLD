#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import re
import util

INIFILE = 'client.ini'

config_changed = False	# To true if config. has changed


class TextMenu:
	def __init__(self):
		self.warning = None # A message displayed
		self.width = 72		# Default menu width
		self.height = 100	# Screen height (used mainly for clear screen)


	def input(self, msg):
		'''Lee una entrada del teclado (a lo BASIC)
		'''
		print msg + ' ',
		return sys.stdin.readline().strip(' \n\t')


	def clearscreen(self):
		'''Clear the console.
    	numlines is an optional argument used only as a fall-back.
    	'''
		if os.name == "posix":
			os.system('clear') # Unix and POSIX OS
		elif os.name in ("nt", "dos", "ce"):
			os.system('cls') # Win32/DOS
		else:
			# Fallback for other operating systems.
			print '\n' * self.height 


	def show(self, options, title = 'MENU'):
		''' Prints the list of options and returns the result selected
		'''
	
		width = self.width - 2
		result = None
	
		while result is None:
			self.clearscreen()
			print 
			print ' +' + '-' * width + '+'
			print ' |' + title.center(width) + '|'
			print ' +' + '-' * width + '+'

			if self.warning is not None:
				width -= 2 # Spaces margin
				ws = [self.warning]

				while len(ws[-1]) > width:
					tmp = ws[-1]
					ws[-1] = tmp[:width]
					ws += [tmp[width:]]

				if len(ws[-1]) < width:
					ws[-1] += ' ' * (width - len(ws[-1]))

				width += 2 # Restore margin
				for i in ws:
					print ' |' + i.center(width) + '|'

				print ' +' + '-' * width + '+'

			print ' |' + ' ' * width + '|'
			print ' |' + 'Type an option and press Enter.'.center(width) + '|'
			print ' |' + 'Leave blank to Cancel.'.center(width) + '|'
			print ' |' + ' ' * width + '|'
		
			count = 0					# Count of the option NUMBER
			for option in (options):	# For every menu option...
				subcount = 0			# Counts the lines for this option
				for i in option.split('\n'):	# Divides the option in lines
					i = i.rstrip(' \t') # Removes remaining tabs and spaces...
					if i == '':			# If it's an empty string...
						s = '' 			# ... the user wants a blank line
					elif i == '-':		# If it is a dash ('-')
						s = '-' * (width - 2)	# The user wants a dashed line ------
					else:				# Otherwise, this is a normal option
						if not subcount:		# If this is the 1st line for this option...
							s = '%2i --> %s' % (count, i)	# prints it with its option number NUMBER --> OPTION text
							count += 1						# and inc. the option number
						else:
							s = ' ' * 7 + i				# else prints the 2nd, 3rd. etc... line for this option

						subcount += 1

					print ' | %s%s |' % (s, ' ' * (width - 2 - len(s)))
		
			print ' |' + ' ' * width + '|'
			print ' +' + '-' * width + '+'
			print
			result = self.input(' Option:')
	
			try:
				if result == '':
					return None
	
				result = int(result)
				if result < 0 or result >= len(options):
					result = None
			except:
				result = None
	
		return result

	
	def confirm(self, msg):
		result = None
		width = self.width - 2
	
		while result is None:
			self.clearscreen()

			print 
			print ' +' + '-' * width + '+'
			print ' |' + 'CONFIRM (Y/N)'.center(width) + '|'
			print ' +' + '-' * width + '+'
			print ' |' + ' ' * width + '|'
			print ' |' + msg.center(width) + '|'
			print ' |' + ' ' * width + '|'
			print ' +' + '-' * width + '+'
			print

			result = self.input(' Type [Y]es or [N]o: ').upper()
			if result not in ['Y', 'N']:
				result = None
		
		return result == 'Y'



class SetupTextMenu(TextMenu):
	def __init__(self, config):
		''' Stores the current configuration. 
		'''
		TextMenu.__init__(self)
		self.cfg = config

	def setup_proxy(self):
		self.warning = None
		menu_title = 'PROXY SETUP'

		option = None
		while option != 0:
			if self.cfg.proxy is None:
				proxy = user = passwd = None
				self.warning = 'No proxy has been defined (Direct Internet Connection)'
				option = menu.show(['Leave proxy undefined (Direct Internet Connection)', 
						'Define a Proxy'], menu_title)

				if option is None: return
			else:
				self.warning = None
				proxy, user, passwd = util.split_proxy_URL(self.cfg.proxy)
				option = menu.show(['Save and Exit',
									'Change proxy url.\nCurrent value: http://%s\n' % proxy,
									'Set proxy user and password\n(Use this if your proxy requires authentication).\nCurrent user: %s' % str(user)],
									menu_title)

			if option == 1:
				proxy = self.input('Proxy url (e.g. http://proxy.organization.com:3128):')
				if proxy == '':
					proxy = None
				else:
					if re.match('http://', proxy): proxy = proxy[7:] # Removes the 'http://' prefix if it exists

			elif option == 2:
				user = self.input('User: [None]')
				if user == '':
					user = passwd = None
				else:
					passwd = self.input('Password: [None]')
					if passwd == '': passwd = None

			if proxy is not None:
				if user is not None:
					proxy = '@' + proxy

					if passwd is not None:
						proxy = ':' + passwd + proxy

					proxy = user + proxy

				self.cfg.proxy = 'http://' + proxy
					

	def setup_brewer(self):
		if self.cfg.options.brewerid is None:
			self.warning = 'WARNING: Brewer ID is *mondatory*'

		option = None
		while option != 0:
			option = menu.show(['Save and Exit','',
						'Set brewer ID.\nCurrent brewer ID: %s' % str(self.cfg.options.brewerid)],
						'BREWER ID SETUP')

			if option is None and self.cfg.options.brewerid is not None:
				break

			if option == 1:
				try:
					self.cfg.options.brewerid = int(self.input('Brewer ID:'))
				except:
					pass


	def setup_working_dir(self):
		if self.cfg.options.rundir is None:
			self.warning = 'WARNING: Working Dir parameter is *mondatory*'

		option = None
		while option != 0:
			option = menu.show(['Save and Exit','',
						'Set Working Directory.\nCurrent is: %s' % str(self.cfg.options.rundir)],
						'WORKING DIRECTORY SETUP')

			if option is None and self.cfg.options.rundir is not None:
				break

			if option == 1:
				rundir = (self.input('Brewer ID:'))
				if not os.path.exists(rundir):
					self.warning = 'WARNING: directory %s does not exists' % rundir
				else:
					if not os.path.isdir(rundir):
						self.warning = 'ERROR: "%s" exists and is not a directory.' % rundir
						rundir = self.cfg.options.rundir
					else:
						self.warning = None

				self.cfg.options.rundir = rundir
		

def save_config(config):
	f = open(INIFILE, 'wt')
	f.write('[global]\n')
	f.write('brewerid = %s\n' % str(config.options.brewerid))
	f.write('working_dir = %s\n' % str(config.options.rundir))

	if config.proxy is not None:	
		f.write('proxy = %s' % config.proxy)

	f.write('\n') # Blank line

	f.close()



try:
	config = util.IniParser(INIFILE)
	config.parseIni()
	menu = SetupTextMenu(config)
except util.IniFileNotExist:
	menu = SetupTextMenu(config)
	menu.warning =  'Warning: File "%s" does not exists. Creating a new one' % INIFILE

option = None

while option != 0:
	option = menu.show([	
		'Save and Exit',
		'', 
		'Setup a proxy (if you are behind a firewall)',
		'Set working directory\n(This is the directory where the client\nstores temporal data)\n', 
		'Setup brewer ID'], 'IBERONESIA CLIENT SETUP')

	if option == 1:
		menu.setup_proxy()
	elif option == 2:
		menu.setup_working_dir()
	elif option == 3:
		menu.setup_brewer()

	if option is None and (not config_changed or menu.confirm('Exit without saving changes. Are you sure?')):
		break

	if option == 0:
		save_config(config)


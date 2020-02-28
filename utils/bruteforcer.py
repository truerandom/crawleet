import parseurls
import time
import random
import string
class bruteforcer:
	def __init__(self,reqobj,extensions,delay,verbose,wordlist=None):
		self.bruteforced = []
		self.req = reqobj
		self.extensions = extensions 
		self.delay = delay
		if self.extensions == []: self.extensions = ['']
		self.verbose = verbose
		self.wordlist = wordlist
		self.words = []
		# global variable for found_resources
		self.found_resources = []
		try:
			with open(self.wordlist) as f:
				self.words = f.read().splitlines()
		except:
			print "Cant open bruteforce wordlist "
			
	"""
	Funcion de bruteforce comun, toma el directorio e itera sobre la lista
	"""
	def directory(self,baseurl):
		blinks = []
		baseurl = self.getPreffix(baseurl)	# chanfle leer solo una vez y cargar en memoria
		if baseurl not in self.bruteforced:
			self.bruteforced.append(baseurl)
			not_found_response = self.get_not_found_response(baseurl)
			if not_found_response is not None:
				if self.verbose: print '[bforcepath]: ',baseurl
				if self.verbose: print '[bruteforcing with %s words]' % len(self.words)
				for lrec in self.words:
					for e in self.extensions:
						res_name = "%s%s" % (lrec,e)
						resource_url = baseurl+res_name if baseurl[-1] == '/' else baseurl+'/'+res_name
						time.sleep(self.delay)
						try:
							resource_response = self.req.s.get(resource_url)
							if self.verbose: print('[i] bruteforcing %s' % resource_url)
							# si stat_code(1) == stat_code(2) => len(1) != len(2)
							# si stat_code(1) != stat_code(2) 
							if resource_response is not None and resource_response.text is not None:
								if not_found_response.status_code != resource_response.status_code:
									print('[+] Bruteforce resource found!: %s' % (resource_url))
									blinks.append(resource_url)
									self.found_resources.append(resource_url)
								else:
									# si son el mismo codigo de estatus hago una nueva peticion
									# con un nombre random del mismo tamanio considerando extensiones
									fixed_name = lrec
									fixed_ext = e
									orig_ext_idx = lrec.rfind('.')
									if orig_ext_idx !=-1:
										fixed_name = lrec[0:orig_ext_idx] 
										fixed_ext = lrec[orig_ext_idx:]
									try:
										not_found_response = self.get_not_found_response(baseurl,len(fixed_name),fixed_ext)
										"""
										print('not_found response status_code %s' % not_found_response.status_code)
										print('not_found_response length: %s' % len(not_found_response.text))
										print('resource_response status_code %s' % resource_response.status_code)
										print('resource response length: %s' % len(resource_response.text))
										"""
										if len(not_found_response.text) != len(resource_response.text):
											print('[+] Bruteforce resource found!: %s' % (resource_url))
											blinks.append(resource_url)
											self.found_resources.append(resource_url)
									except Exception as e:
										print(e)
						except Exception as e:
							print(e)
							exit()
			return blinks
		else:
			if self.verbose: print 'Bruteforcer@directory %s Skipping directory (already bruteforced)' % baseurl
		return blinks
	
	def get_not_found_response(self,dir_url,name_length=32,ext=''):
		random_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(name_length)])
		random_url = '%s%s%s' % (dir_url,random_str,ext)
		#print('Generated random_url %s' % random_url)
		try:
			r = self.req.s.get(random_url)
			if r is not None and r.text is not None:
				return r
			return None
		except Exception as e:
			print('[i] problem with %s' % random_url)
			print(e)
			return None
		
	# Regresa el prefijo del recurso ie url de url/recurso
	def getPreffix(self,baseurl):
		# El problema ocurre aqui debo ver si el preffix es de un recurso
		return baseurl.rsplit('/',1)[0]+'/'
	
	"""
	Utilizado para encontrar respaldos del recurso pasado como parametro
	"""
	def thisFile(self,baseurl):
		blinks = []
		resname = parseurls.getRecFinal(baseurl)
		baseurl = self.getPreffix(baseurl)	# chanfle leer solo una vez y cargar en memoria
		filebackups = parseurls.getBackupNames(resname)

		not_found_response = self.get_not_found_response(baseurl)
		if not_found_response is not None and not_found_response.text is not None:
			for fbak in filebackups:
				backup_url = baseurl+fbak if baseurl[-1] == '/' else baseurl+'/'+fbak
				try:
					response_backup_url = self.req.s.get(backup_url)
					if response_backup_url is not None and response_backup_url.text is not None:
						if len(not_found_response.text) != len(response_backup_url.text):
							blinks.append(response_backup_url)
				except Exception as e:
					print(e)

			"""
			stat = self.req.getHeadRequest(res).status_code
			if stat is not None and stat < 300:
				print "[+] Resource found: %s",res
				blinks.append(res)
			"""
		return blinks
		
	def __str__(self):
		s = "*"*30+"\n"+"Bruteforcer"+"\n"
		print s
		print self.req
		print self.wordlist
		return ""

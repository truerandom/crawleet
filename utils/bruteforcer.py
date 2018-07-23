import parseurls
import time
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
		try:
			with open(self.wordlist) as f:
				self.words = f.read().splitlines()
		except: print "Cant open bruteforce wordlist "
	
	def directory(self,baseurl):
		blinks = []
		baseurl = self.getPreffix(baseurl)	# chanfle leer solo una vez y cargar en memoria
		if baseurl not in self.bruteforced:
			self.bruteforced.append(baseurl)
			if self.verbose: print '[bforcepath]: ',baseurl
			if self.verbose: print '[bruteforcing with %s words]' % len(self.words)
			for lrec in self.words:
				for e in self.extensions:
					resource = baseurl+str(lrec)+e if baseurl[-1] == '/' else baseurl+'/'+str(lrec)+str+e
					#if self.verbose: print '[Asking for] %s' % (resource)
					time.sleep(self.delay)
					try:
						stat = self.req.getHeadRequest(resource).status_code
						if stat is not None and stat < 300:
							if self.verbose: print "Resource found -> ",resource
							blinks.append(resource)
					except:
						return []
		else:
			if self.verbose: print 'Bruteforcer@directory %s Skipping directory (already bruteforced)' % baseurl
		return blinks
	
	# Regresa el prefijo del recurso ie url de url/recurso
	def getPreffix(self,baseurl):
		# El problema ocurre aqui debo ver si el preffix es de un recurso
		return baseurl.rsplit('/',1)[0]+'/'
		
	def thisFile(self,baseurl):
		blinks = []
		resname = parseurls.getRecFinal(baseurl)
		baseurl = self.getPreffix(baseurl)	# chanfle leer solo una vez y cargar en memoria		
		filebackups = parseurls.getBackupNames(resname)
		for fbak in filebackups:
			res = baseurl+fbak if baseurl[-1] == '/' else baseurl+'/'+fbak
			stat = self.req.getHeadRequest(res).status_code
			if stat is not None and stat < 300:
				print "[+] Resource found: %s",res
				blinks.append(res)
		return blinks
		
	def __str__(self):
		s = "*"*30+"\n"+"Bruteforcer"+"\n"
		print s
		print self.req
		print self.wordlist
		return ""

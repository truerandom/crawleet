'''
Clase para realizar peticiones html
Hace falta pasar el user agent
'''
import requests
import sys
import re
class rutils:
	'''
	Constructor
	verificar:	bandera para verificar los certificados
	redirects:	permitir redirecciones
	cookies:	cookies a usar en las peticiones
	uagent:		user agent
	tor:		utilizar tor o no
	proxy:		proxy a utilizar
	timeout:	por default .5
	'''
	def __init__(self,verificar=True,redirects=False,cookies=None,uagent=None,tor=False,timeout=1,proxy=None):
		self.verificar = verificar
		# sesion de requests
		self.s = requests.Session()
		self.verificar = verificar
		self.s.verify = self.verificar
		self.s.allow_redirects = redirects
		self.tor = tor
		self.timeout = timeout 
		# metodo para obtener la cookie en un diccionario a partir de una cadena
		if cookies is not None:
			galleta = self.getCookies(cookies)
			self.s.cookies.update(galleta)
		if uagent is not None:
			uag = self.s.headers['User-Agent'] = uagent
		else:
			self.s.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko'}
		if self.tor:
			self.s.proxies = {'http':'socks5://127.0.0.1:9050','https':'socks5://127.0.0.1:9050'}
		if proxy is not None:
			self.s.proxies = self.getProxies(proxy)
		# Aqui obtengo la ip desde la que se realiza el escaneo
		self.config()
		
	def __str__(self):
		tmp='\nRequest Object'
		tmp+='\nRedirects: %s'%(self.s.allow_redirects)
		tmp+='\nVerificarCerts: %s\nRedirects: %s' % (self.s.verify,self.s.allow_redirects)
		tmp+='\nTimeout: %s' % self.timeout
		tmp+='\nCookies: %s' % (self.s.cookies)
		tmp+='\nUserAgent %s ' % (self.s.headers['User-Agent'])
		tmp+='\nTor: %s' % (self.tor)
		tmp+="\nProxies: %s " % (self.s.proxies)
		tmp+="\nTimeout: %s " % self.timeout
		tmp+='\n'
		return tmp

	def config(self):
		reload(sys)
		sys.setdefaultencoding('utf8')
		try:
			self.ip = self.getHTMLCode('http://myexternalip.com/raw').text
		except:
			self.ip = '127.0.0.1'
		try:
			if not self.verificar:
				requests.packages.urllib3.disable_warnings()
		except:
			if self.verbose: print 'Cant disable urllib3 warns'

	#################### Modify #################################
	# chanfle union
	def getHTMLCode(self,direccion):
		try:
			r = self.s.get(direccion,timeout=self.timeout)
			return r
		except:
			return None

	def getHeadRequest(self,direccion):
		try:
			r = self.s.head(direccion,timeout=self.timeout)
			return r
		except:
			return None
	
	# metodo que regresa un diccionario con las cookies pasadas como cadena
	def getCookies(self,cookie):
		if cookie is not None:
			cookies = {}
			for c in cookie.split(';'):
				elem = c.split('=')
				cookies[elem[0]] = ''.join(elem[1:])
			return cookies
		return {}
		
	# regresa un diccionario con los proxys definidos en la cadena param
	# donde la cadena tiene la forma "protocolo://ip:port;[proto://ip:port]*"
	def getProxies(self,proxies):
		pxysdict = {}
		pxys = proxies.split(';')
		for pxy in pxys:
			proto = pxy.split(':')[0]
			ipadd = "".join(pxy.split('//')[1:])
			pxysdict[proto] = ipadd
		return pxysdict

	#################### new methods ###########################
	def test_OPTIONS(self,host):
		try:
			req = self.s.request('OPTIONS',host,timeout=self.timeout)
			if req.status_code == 200 and req.reason == 'OK' and 'Allow' in req.headers.keys(): # y allow
				return req.headers['Allow']
			return None
		except Exception as e:
			print e
			return None

	def test_Method(self,host):
		try:
			print("entre a test_Method")
			exit(0)
		except Exception as e:
			print(e)
			return None

	# Regresa un diccionario con los metodos disponibles en el servidor
	# web. Donde la llave es el metodo y el valor los headers de respuesta
	def getMethods(self,host):
		"""
		supportedm = {}
		methods=[self.test_GET,
			self.test_OPTIONS,
			]
		for m in methods:
			print m
			res = m(host)
		return supportedm
		"""
		methods = ['GET','OPTIONS','PUT','OPTIONS','TRACE']
		supportedm = {}
		for m in methods:
			try:
				resp = self.s.request(m,host,timeout=self.timeout)
				if resp.status_code == 200 and resp.reason == 'OK':
					supportedm[m] = resp.headers
			except:
				print 'Method not supported %s'%m
		return supportedm
	def redirects(self): return self.s.allow_redirects
	def verifyCert(self): return self.s.verify
	def cookies(self): return self.s.cookies
	def userAgent(self): return self.s.headers['User-Agent']
	def useTor(self): return self.tor
	def getIP(self): return self.ip
	def getProxys(self): return self.s.proxies
	def getTimeout(self): return self.timeout

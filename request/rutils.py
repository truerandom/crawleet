'''
Clase para realizar peticiones html
Hace falta pasar el user agent
'''
import requests
import sys
import re
from utils import parseurls
import socket
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

	#################### methods testing ###########################
	def test_OPTIONS(self,host):
		try:
			req = self.s.request('OPTIONS',host,timeout=self.timeout)
			if req.status_code == 200 and req.reason == 'OK' and 'Allow' in req.headers.keys(): # y allow
				return req.headers
			return None
		except Exception as e:
			return None
			
	def test_GET(self,host):
		try:
			req = self.s.request('GET',host,timeout=self.timeout)
			if req.status_code == 200 and req.reason == 'OK': # y allow
				return req.headers
			return None
		except Exception as e:
			return None
			
	def test_PUT(self,host):
		try:
			req = self.s.request('PUT',host,timeout=self.timeout)
			if req.status_code == 200 and req.reason == 'OK': # y allow
				return req.headers
			return None
		except Exception as e:
			return None
			
	def test_TRACE(self,host):
		try:
			req = self.s.request('TRACE',host,timeout=self.timeout)
			if req.status_code == 200 and req.reason == 'OK': # y allow
				return req.headers
			return None
		except Exception as e:
			return None
			
	def test_POST(self,host):
		try:
			req = self.s.request('POST',host,timeout=self.timeout)
			if req.status_code == 200 and req.reason == 'OK': # y allow
				return req.headers
			return None
		except Exception as e:
			return None

	def test_Method(self,host):
		try:
			exit(0)
		except Exception as e:
			print(e)
			return None

	# Regresa un diccionario con los metodos disponibles en el servidor
	# web. Donde la llave es el metodo y el valor los headers de respuesta
	def getMethods(self,host):
		supportedm = {}
		methods={self.test_GET:"GET",
			self.test_OPTIONS:"OPTIONS",
			self.test_POST:"POST",
			self.test_PUT:"PUT",
			self.test_TRACE:"TRACE",
			}
		for method in methods.keys():
			res = method(host)
			if res is not None:
				supportedm[methods[method]] = res
		return supportedm
		
	def savePage(self,page,finame=None):
		try:
			r = self.getHTMLCode(page)
			if r is not None and r.text is not None:
				dom = parseurls.domainOnly(page)
				if finame is None:
					finame = '%s_saved.html' % dom
				f = open(finame,"w")
				f.write(r.text)
				f.close()
		except Exception as e:
			print e
			
	def getSiteIP(self,page):
		try:
			dom = parseurls.domainOnly(page)
			act_ip = socket.gethostbyname(dom)
			return str(act_ip)
		except Exception as e:
			print e
			return ""
	
	# Used by SQLi 
	def word_not_in_response(self,words,url):
		try:
			words_not_found = []
			r = self.getHTMLCode(url)
			if r is not None and r.text is not None:
				for word in words:
					if word.lower() not in r.text.lower():
						words_not_found.append(word)
				return words_not_found
			else:
				return []
		except Exception as e:
			print e
			# Something happens, we assume we dont know anything about url
			return []
			
	def redirects(self): return self.s.allow_redirects
	def verifyCert(self): return self.s.verify
	def cookies(self): return self.s.cookies
	def userAgent(self): return self.s.headers['User-Agent']
	def useTor(self): return self.tor
	def getIP(self): return self.ip
	def getProxys(self): return self.s.proxies
	def getTimeout(self): return self.timeout

#!/usr/bin/env python2
import requests
import subprocess
import re
from subprocess import check_output
from utils import parseurls
try:
	from colorama import init, Fore,Back, Style
except:
	pass

class detector(object):
	def __init__(self,req=None,datadir=None,color=False):
		try: init(convert=True,autoreset=True) # colorama
		except: pass
		self.color = False
		# new
		self.datadir = datadir
		self.name = 'detector'
		self.headers = []
		self.filelist = []
		self.wordpatterns = []
		# Objeto para realizar las peticiones
		self.req = req
		# holder cms root
		self.cmsroot = None
		# flags to search in external tool output
		self.toolflags = []
		self.toolargs = []
		self.toolpath = None
		# Salida de la herramienta externa
		self.output = None
		
		self.defaultdirs = []
		self.defaultfiles = []
		self.dicdefdirs = {}
		self.detections = []
		# Bandera para hacer postcrawl cada modulo hara su funcion especifica
		self.postcrawl = False
		# Puntuacion del detector
		self.puntuation = 0	
	
	#working
	def getName(self):
		return self.name
	
	#working
	def setToolPath(self,toolpath):
		if toolpath is not None: self.toolpath = toolpath
	
	def setToolArgs(self,toolargs):
		if toolargs is not None: self.toolargs = toolargs
		
	def setToolFlags(self,toolflags):
		if toolflags is not None: self.toolflags = toolflags

	def launchTool(self): 
		#print "entre a launchtool "
		if self.toolpath is not None:
			#print "toolpath ",self.toolpath
			# toolargs settings
			try:
				# cambio el placeholder por la url
				if self.toolflags is not None:
					print 'Tool flags -> ',self.toolflags
				for i in range(0,len(self.toolargs)):
					if self.toolargs[i] == '{url}': 
						if self.cmsroot is not None:
							self.toolargs[i] = self.cmsroot
						else:
							self.toolargs[i] = self.detections[0]
				print 'Ejecutando herramienta externa:'
				print ' '.join(self.toolargs)
				print 'Wait external scan in progress'
				ps = subprocess.Popen((self.toolargs), stdout=subprocess.PIPE)
				output, err = ps.communicate()
				self.output = output
				# Aqui debo actualizar la puntuacion del detector
				self.extToolScore()
				return self.name+'tool\n'+output
			except Exception as e:
				print 'Error running -> ',self.toolpath,' -> ',e
		else:
			print 'No external tool defined for ',self.name
	
	def extToolScore(self):
		for tflag in self.toolflags:
			marker = tflag[0]
			score = tflag[1]
			count = self.output.count(marker)
			self.puntuation+=count*score
		print "*"*50,"Module Puntuation: %s "%(self.name),self.puntuation,"*"*50
		
	# Busca por la carga del header h:key busca key
	def fromHeaders(self,rheaders,direccion):
		rhead,rhkeys = rheaders,rheaders.keys()
		for lheader in self.headers:
			for rhkey in rhkeys:
				if lheader in rhead[rhkey]:
					# aqui lo agrego a la lista
					if self.color:
						try:
							print (Fore.GREEN+'Sw found (Header detection) >>>>>>>> '+Fore.RED+self.name+Style.RESET_ALL)
						except:
							print 'Sw found (Header detection) >>>>>>>> ',self.name
					else:
						print 'Sw found (Header detection) >>>>>>>> ',self.name
					if direccion not in self.detections:
						self.detections.append(direccion)
						self.puntuation+=.1
					return True
		return False
	
	# Busca las cadenas (regexp) de wordpatterns en el codigo html
	def fromCode(self,rcode,direccion):
		for wp in self.wordpatterns:
			matches = re.findall(wp,rcode,re.IGNORECASE) 
			if len(matches) > 0:
				if self.color:
					try:
						print (Fore.GREEN+'Sw found (Code detection) >>>>>>>> '+Fore.RED+self.name+Style.RESET_ALL)
					except:
						print 'Sw found (Code detection) -> ',self.name
				else:
					print 'Sw found (Code detection) -> ',self.name
				# debug
				print matches
				for m in matches:
					if m not in self.detections:
						temp = direccion
						self.detections.append(temp)
						self.puntuation+=.1
				return True
		return False
	
	# Detecta mediante la url (nombre del archivo)
	def fromFilename(self,filename):
		for f in self.filelist:
			if f in filename:
				if filename not in self.detections:
					self.detections.append(filename)
					self.puntuation+=.1
				if self.color:
					try:
						print (Fore.GREEN+'Sw found (Path detection) -> '+Fore.RED+self.name+Style.RESET_ALL)
					except:	
						print 'Sw found (Path detection) -> ',self.name
				else:
					print 'Sw found (Path detection) -> ',self.name
				# debug
				print 'matched: {%s} ' % f
				return True
		return False
	
	def hasDetections(self):
		if len(self.detections) > 0:
			return True
		return False
	
	def getResults(self):
		if self.hasDetections():
			return self.detections
	
	# chanfle: cross calling
	def getResources(self):
		#print 'entre a Swdetection@getResources ',self.name
		try:
			if self.cmsroot is not None:
				#print 'cmsroot no es None',self.cmsroot
				#print 'cmsroot no es None',self.cmsroot	# da problemas si quito el self se soluciona
				return self.name,self.getResults(),self.cmsroot
			return self.name,self.getResults()
		except Exception as e:
			return self.name,self.getResults()
				
	# inicializa el diccionario con los directorios default del cms
	def initDicDefDirs(self):
		for defdir in self.defaultdirs:
			self.dicdefdirs[defdir] = 1

	# returns not default cms directories
	def postCrawling(self):
		if self.postcrawl:
			#print 'entre a swdetect postcrawling ',self.name
			#print 'debug self.detections ',self.detections
			# Directorios encontrados
			dirs = parseurls.getDirectories(self.detections)
			print('found dirs: ')
			print('\n'.join(dirs))
			################### DIRECTORIOS NO COMUNES #################
			uncommon = parseurls.uncommonDirectories(dirs,self.defaultdirs)
			if len(uncommon)>0:
				print('Uncommon directories:')
				print('\n'.join(uncommon))
				# Agrego esto a las detecciones
				self.detections+=['...']+['Uncommon Dirs: ']+uncommon
			######### BUSQUEDA DE ARCHIVOS DE CMS EN LOS DIRS ##########
			#print "\n","*"*30," "+self.name+" bruteforcing ","*"*30
			if self.color:
				try: print(Fore.BLUE+'\n'+self.name+" bruteforcing "+Style.RESET_ALL)
				except: print '\n',self.name+" bruteforcing: "
			else:
				print '\n',self.name+" bruteforcing: "
			# inicializo el diccionario de directorios default
			self.initDicDefDirs()
			# obtengo la raiz del cms
			#print 'SWDETECTION@CMSROOT ',self.name
			#print 'dirs ',dirs
			cmsroot = parseurls.getCMSRoot(dirs,self.dicdefdirs)
			#print 'debug swdetction cmsroot ',cmsroot
			if cmsroot is not None:
				#print "CMSROOT ",cmsroot
				self.cmsroot = cmsroot
				files = self.defaultfiles
				filesfound = []
				# peticiones a los archivos del cms juicyfiles
				for f in files:
					scode = -1
					try:
						scode = self.req.getHTMLCode(cmsroot+f).status_code
					except Exception as e:
						print "Error getting %s " % (cmsroot+f)
					if scode == 200 or scode == 405:
						#print '*'*10,cmsroot+f,'*'*10
						print cmsroot+f
						self.puntuation+=1
						filesfound.append(cmsroot+f)
				if len(filesfound)>0:
					self.detections+=['...']+['Files found: ']+filesfound
				themesfound = []
				# peticiones a los archivos del cms juicyfiles
				for theme in self.themes:
					scode = -1
					try:
						scode = self.req.getHTMLCode(cmsroot+theme).status_code
					except Exception as e:
						print "Error getting %s " % (cmsroot+f)
					if scode == 200 or scode == 405:
						print cmsroot+theme
						#print '*'*10,cmsroot+theme,'*'*10
						self.puntuation+=1
						themesfound.append(cmsroot+theme)
				if len(filesfound)>0:
					self.detections+=['...']+['Themes found: ']+themesfound
		# aqui paso los recursos detectados por el modulo a los modulos de vulnerabilidades
		return self.getResources()
				
	# Regresa el resultado de la herramienta externa
	def getExternalResults(self):
		if self.output is not None:
			return self.name +'ExtTool'+'\n' + self.output
	
	#
	def getPuntuation(self):
		return self.puntuation
		
	def getName(self):
		return self.name
		
	#working
	def __str__(self):
		return 'Name: %s\nHeaders: %s\nFlist: %s\nWPat: %s\nTPath: %s\nToolArgs: %s'%(self.name,self.headers,self.filelist,self.wordpatterns,self.toolpath,self.toolargs)
	
class genscan(detector):
	#def __init__(self,req,datadir,name,color=False):
	# self,req,color,datadir,name,filelist,dirs,juicyfiles,postCrawl
	def __init__(self,req,color,datadir,name,headers,wordpatterns,filelist,dirs,juicyfiles,themes,postcrawl):
		self.name = name
		self.req = req
		# new
		self.datadir = datadir
		self.color = color
		self.cmsroot = None
		self.headers = []
		self.wordpatterns = wordpatterns
		self.filelist = filelist
		self.defaultdirs = dirs
		self.defaultfiles = juicyfiles
		self.themes = themes
		self.postcrawl = postcrawl
		self.dicdefdirs = {}
		self.detections = []
		self.toolflags = []
		self.toolpath = None
		self.toolargs = []
		self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		
class mailscan(detector):
	def __init__(self,req=None,color=False):
		self.name = 'mail'
		self.color = color
		self.req = req
		self.headers = []
		# regex mailto
		self.filelist = ['mailto:(.*)']
		# self.wordpatterns = [('[A-Za-z_\.0-9]+@[A-Za-z0-9]+\.[A-Za-z]+')]
		self.wordpatterns = [('[A-Za-z_\.0-9]+@[A-Za-z0-9]+\.[A-Za-z\.]+')]
		self.toolpath = None
		self.postcrawl = False
		self.detections = []
		self.toolargs = []
		self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		
	def fromFilename(self,filename):
		for f in self.filelist:
			matches = re.findall(f,filename,re.IGNORECASE) 
			if len(matches) > 0:
				for m in matches:
					if self.color:
						try:
							print (Fore.GREEN+"Mail found (Code detection) "+Fore.RED+m+Style.RESET_ALL)
						except:
							print 'Mail found (Code detection) -> ',m
					else:
						print 'Mail found (Code detection) -> ',m
					if m not in self.detections:
						self.detections.append(m)
						self.puntuation+=.1
				return True
		return False

	# Busca las cadenas (regexp) de wordpatterns en el codigo html
	def fromCode(self,rcode,direccion):	
		for wp in self.wordpatterns:
			matches = re.findall(wp,rcode,re.IGNORECASE) 
			if len(matches) > 0:
				#for m in matches:
				for m in set(matches):
					if self.color:
						try:
							print (Fore.GREEN+"Mail found (Code detection) "+Fore.RED+m+Style.RESET_ALL)
						except:
							print 'Mail found (Code detection) -> ',m
					else:
						print 'Mail found (Code detection) -> ',m
					if m not in self.detections:
						#print m
						self.detections.append(m)
						self.puntuation+=.1
				return True
		return False

class contentscan(detector):
	def __init__(self,req=None,color=False):
		self.name = 'content'
		self.color = color
		self.req = req
		self.headers = []
		# regex mailto
		self.filelist = ['admin','admon','password','passwd','pwd',
			'login','logon','curp','rfc','cuenta','shadow','info','action']
		self.wordpatterns = ['(adm[io]n[A-Za-z0-9\t. ]{3,})',
		'((us(er[s]|r))[A-Za-z0-9\t. ]{5,})',
		'((passw(or)?d)[A-Za-z0-9\t. ]{5,})','(pwd[A-Za-z0-9\t. ]{5,})',
		'(log[io]n[A-Za-z0-9\t. ]{5,})','(curp[A-Za-z0-9\t. ]{5,})',
		'(rfc[A-Za-z0-9\t. ]{5,})','(cuenta[A-Za-z0-9\t. ]{5,})',
		'((usuario[s]?)[A-Za-z0-9\t. ]{5,})']
		self.toolpath = None
		self.postcrawl = False
		self.detections = []
		self.toolargs = []
		self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		
	def fromFilename(self,filename):
		for f in self.filelist:
			matches = re.findall(f,filename,re.IGNORECASE) 
			if len(matches) > 0:
				for m in matches:
					if self.color:
						try:
							print (Fore.GREEN+"Content found (Path detection) ->"+Fore.RED+m+Style.RESET_ALL)
						except:
							print 'Content found (Path detection) -> ',m
					else:
						print 'Content found (Path detection) -> ',m
					#print 'Content found (Path detection) -> ',m
					if m not in self.detections:
						self.detections.append(filename)
						self.puntuation+=1
				return True
		return False
		
	# Busca las cadenas (regexp) de wordpatterns en el codigo html
	def fromCode(self,rcode,direccion):	
		for wp in self.wordpatterns:
			matches = re.findall(wp,rcode,re.IGNORECASE) 
			if len(matches) > 0:
				#for m in matches:
				currentdetect = '%s -> %s' % (direccion,(matches))
				print currentdetect
				self.detections.append(currentdetect)
				self.puntuation+=1
				return True
		return False

class backupscan(detector):
	def __init__(self,req=None,color=False):
		self.name = 'backup'
		self.color = color
		self.req = req
		self.headers = []
		# regex mailto
		#self.filelist = [".bak",".back",".copia",".old",".res",".temp",
		#".tmp","respaldo",".anterior"]
		self.filelist = ["\.bak","\.back","\.copia","\.old","\.res","\.temp",
		"\.tmp","respaldo","\.anterior","respaldo"]
		self.wordpatterns = []
		self.toolpath = None
		self.postcrawl = False
		self.detections = []
		self.toolargs = []
		self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		
	def fromFilename(self,filename):
		for f in self.filelist:
			matches = re.findall(f,filename,re.IGNORECASE) 
			if len(matches) > 0:
				for m in matches:
					if self.color:
						try:
							print (Fore.GREEN+"Content found (Path detection) ->"+Fore.RED+m+Style.RESET_ALL)
						except:
							print 'Content found (Path detection) -> ',m
					else:
						print 'Content found (Path detection) -> ',m
					#print 'Content found (Path detection) -> ',m
					if m not in self.detections:
						self.detections.append(filename)
						self.puntuation+=1
				return True
		return False
		
	# Busca las cadenas (regexp) de wordpatterns en el codigo html
	def fromCode(self,rcode,direccion):	
		for wp in self.wordpatterns:
			matches = re.findall(wp,rcode,re.IGNORECASE) 
			if len(matches) > 0:
				#for m in matches:
				currentdetect = '%s -> %s' % (direccion,(matches))
				print currentdetect
				self.detections.append(currentdetect)
				self.puntuation+=1
				return True
		return False

class paramscanner(detector):
	def __init__(self,req=None,color=False):
		self.name = 'parameter scanner'
		self.color = color
		self.req = req
		self.headers = []
		# regex mailto
		self.filelist = []
		self.wordpatterns = []
		self.toolpath = None
		self.postcrawl = False
		self.detections = []
		self.toolargs = []
		self.params = {}
		self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		
	# Regresa si una url esta enviando parametros via GET
	def sendParams(self,url):
		if len(url.split('?')) > 1:
			return True
		return False

	# Regresa una tupla (baseurl,params)
	# params es una lista de parametros; [p1=algo2,p2=algo2,p3=algo3]
	def getFields(self,url):
		fields = url.split('?')
		baseurl = fields[0]
		params = ''.join(fields[1:]).split('&')
		return (baseurl,params)
	
	# No me acuerdo que hace xD :/	
	def fillData(self,url):
		if self.sendParams(url) == True:
			data = self.getFields(url)
			baseurl = data[0]
			if baseurl not in self.params:
				self.params[baseurl] = []
			for p in data[1]:
				if p not in self.params[baseurl]:
					self.params[baseurl].append(p)
	
	def hasDetections(self):
		if len(self.params.keys()) > 0:
			return True
		return False
	
	# debe regresar una lista
	# [params, url:(p1,p2,...pn), url:(px1,px2...px3)]
	def getResults(self):
		llaves = self.params.keys()
		#tmp = [self.name]
		tmp = []
		for llave in llaves:
			tmp.append('\n'+llave+':\n\t'+'\n\t->['.join(sorted(self.params[llave]))+']')
		return tmp
		
	def fromFilename(self,filename):
		self.fillData(filename) 
		return False


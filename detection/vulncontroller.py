#!/usr/bin/env python2
import requests
from vulndetection import *
from config.ConfigParser import *
from utils import parseurls

# Controlador para los detectores de vulnerabilidades
class vulncontroller:
	#def __init__(self,configfile,detectors = None):
	# objeto para peticiones
	def __init__(self,configfile,req,color=False,detectors = None):
		self.configfile = configfile
		self.color = color
		self.detectors = detectors
		self.req = req
		self.tools = []
		self.configparser = ConfigParser(self.configfile)
		self.initTools()
		
	def setConfFile(self,configfile):
		if configfile is not None: self.configfile = configfile
	
	# Aqui solo pongo los detectores pasados como parametros
	def setDetectors(self,detectors):
		if detectors is not None:
			self.detectors = detectors
	
	# define los modulos de deteccion a ocupar
	def initTools(self):
		strutscanner =  strutscan(self.req,self.color)
		drupalscanner =  drupalscan(self.req,self.color)
		wordpresscanner = wordpresscan(self.req,self.color)
		joomlascanner = joomlascan(self.req,self.color)
		moodlescanner = moodlescan(self.req,self.color)
		magentoscanner = magentoscan(self.req,self.color)
		self.tools = [strutscanner,drupalscanner,wordpresscanner,joomlascanner,moodlescanner,magentoscanner]		
		
	def fromHeaders(self,rheaders,direccion):
		for tool in self.tools:
			tool.fromHeaders(rheaders,direccion)

	def fromCode(self,rcode,direccion):
		for tool in self.tools:
			tool.fromCode(rcode,direccion)

	def fromFilename(self,filename):
		for tool in self.tools:
			tool.fromFilename(filename)
	
	# regresa una lista con los resultados de las herramientas externas
	# de cada modulo
	def runExtTools(self):
		"""
		extres = []
		for tool in self.tools:
			if tool.hasDetections():
				extr = tool.launchTool()
				if extr is not None:
					extres.append(extr)
		return extres
		"""
		return []
		
	# regresa la suma de la puntuacion de los modulos		
	def getPuntuation(self):
		score = 0
		for tool in self.tools:
			score+= tool.getPuntuation()
		return score
		
	def results(self):
		temp = []
		for tool in self.tools:
			if tool.hasDetections():
				temp.append([tool.name]+tool.getResults())
		return temp
		
	# Recibe una tupla (nombredelmoduloquedetecto,listaderecursos,cmsroot posible nulo)
	def setResources(self,detectorname,resources,cmsroot=None):
		"""
		print '****'
		print 'entre a VulnController@setResources con\n%s\n%s\ncmsroot%s' % (detectorname,resources,cmsroot)
		print 'setting Resources'
		print 'we have %s vuln modules ' % (len(self.tools)),' ',self.tools
		print '****'
		"""
		for tool in self.tools:
			if detectorname == tool.getName():
				#print 'Setting resources to ',tool.getName()
				tool.setResources(resources,cmsroot)
				# una vez que le paso los recursos ejecuta los exploits
				tool.launchExploitsF()
		
	
	# postcrawling, aqui obtengo los directorios no comunes y consulto los archivos default
	# solo se hace para los modulos que tuvieron detecciones
	def postCrawling(self):
		pass
		"""
		for tool in self.tools:
			if tool.hasDetections():
				tool.postCrawling()
		"""
		
	# Regresa una lista con los resultados de las herramientas externas
	def externalResults(self):
		return []
		"""
		print '*'*70
		temp = []
		for tool in self.tools:
			# lista de cadenas
			tmp = tool.getExternalResults()
			if tmp is not None: temp.append(tmp)
		# lista de cadenas
		return temp
		"""
		
	def __str__(self):
		temp = ''
		for tool in self.tools: temp+='\n'+tool.name
		return 'Detectors available'+temp+'\n'

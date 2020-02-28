#!/usr/bin/env python2
import requests
from vulndetection import *
from config.ConfigParser import *
from utils import parseurls

# Controlador para los detectores de vulnerabilidades
class vulncontroller:
	#def __init__(self,configfile,detectors = None):
	# objeto para peticiones
	# TODO: include blacklist
	def __init__(self,configfile,blacklist,req,color=False,detectors = None):
		self.configfile = configfile
		self.blacklist = parseurls.getList(blacklist)
		print('vulncontroller: %s' % configfile)
		print('Cfgfile %s' % configfile)
		print('Blacklist %s' % blacklist)
		print('type blacklist %s' % type(blacklist))
		print('color %s' % color)
		print('len blacklist %s' % len(self.blacklist))
		self.req = req
		self.color = color
		self.configparser = ConfigParser(self.configfile)
		self.tools = []
		self.initTools()
	
	def setConfFile(self,configfile):
		if configfile is not None: self.configfile = configfile
	
	# define los modulos de deteccion a ocupar
	def initTools(self):
		print('en initTools')
		strutscanner =  strutscan(self.req,self.blacklist,self.color)
		drupalscanner =  drupalscan(self.req,self.blacklist,self.color)
		wordpresscanner = wordpresscan(self.req,self.blacklist,self.color)
		joomlascanner = joomlascan(self.req,self.blacklist,self.color)
		moodlescanner = moodlescan(self.req,self.blacklist,self.color)
		magentoscanner = magentoscan(self.req,self.blacklist,self.color)
		# nuevo modulo 
		xssscanner = xssscan(self.req,self.blacklist,self.color)
		sqliscanner = sqliscan(self.req,self.blacklist,self.color)
		path_tscan = path_traversal_scan(self.req,self.blacklist,self.color)
		self.tools = [strutscanner,drupalscanner,wordpresscanner,joomlascanner,
		moodlescanner,magentoscanner,xssscanner,sqliscanner,path_tscan]		
		
	def fromHeaders(self,rheaders,direccion):
		for tool in self.tools:
			tool.fromHeaders(rheaders,direccion)

	def fromCode(self,rcode,direccion):
		for tool in self.tools:
			tool.fromCode(rcode,direccion)

	def fromFilename(self,filename):
		for tool in self.tools:
			tool.fromFilename(filename)
	
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
		
	def __str__(self):
		temp = ''
		for tool in self.tools: temp+='\n'+tool.name
		return 'Detectors available'+temp+'\n'

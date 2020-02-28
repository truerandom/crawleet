#!/usr/bin/env python2
from xml.dom.minidom import parse
import requests
from swdetection import *
#from ConfigParser import *
from config.ConfigParser import *
from utils import parseurls

# Controlador para los detectores de contenido
class swcontroller:
	#def __init__(self,configfile,detectors = None):
	# objeto para peticiones
	# swcontroller tiene un objeto vulncontroller
	# def __init__(self,configfile,configdir,req,vulncontroller,color=False,detectors = None):
	def __init__(self,configfile,datadir,req,vulncontroller,color=False,detectors = None):
		self.configfile = configfile
		self.datadir = datadir
		self.vulncontroller = vulncontroller
		self.color = color
		self.detectors = detectors
		self.req = req
		self.tools = []
		self.configparser = ConfigParser(self.configfile)
		self.initTools()
		
	def setConfFile(self,configfile):
		if configfile is not None: self.configfile = configfile
	
	# Aqui solo pongo los detectores pasados como parametros
	"""
	def setDetectors(self,detectors):
		if detectors is not None: self.detectors = detectors
	"""
	
	# define los modulos de deteccion a ocupar
	def initTools(self):
		# wordpatterns,files,directories,headers,juicyfiles,postcrawling
		scanners = []
		swmods = self.getSoftwareModules()
		for sw in swmods.keys():
			wpatterns = swmods[sw][0]
			files = swmods[sw][1]
			dirs = swmods[sw][2]
			headers = swmods[sw][3]
			juicyfiles = swmods[sw][4]
			postcrawling = swmods[sw][5]
			themes = swmods[sw][6]
			actscan = genscan(self.req,self.color,self.datadir,sw,headers,
			wpatterns,files,dirs,juicyfiles,postcrawling,themes)
			actscan.setToolPath(self.configparser.getPath(sw))
			actscan.setToolArgs(self.configparser.getToolArg(sw))
			actscan.setToolFlags(self.configparser.getToolFlags(sw))
			scanners.append(actscan)
		mail = mailscan(self.req,self.color)
		params = paramscanner(self.req,self.color)
		content = contentscan(self.req,self.color)
		backscan = backupscan(self.req,self.color)
		self.tools = scanners+[mail,params,content,backscan]
		#self.tools = [wordpress,drupal,moodle,joomla,ojs,magento,mail,params,content,backscan]		
	
	# Regresa un diccionario con los softwares a identificar y como identificarlos
	# {'nombresoftware':[wpatterns],[files],[directories],[headers],[juicydata],postcrawling}
	# esto para aprovechar la herencia y no tener un constructor de cada
	# cms, sino iterar por nombre en el diccionario y pasar las listas
	# como datos al constructor de cada software en swdetection
	# # wordpatterns,files,directories,headers,juicyfiles,postcrawling
	def getSoftwareModules(self):
		dom = parse(self.datadir)
		# diccionario para las herramientas
		sw = {}
		xmltools=dom.getElementsByTagName('software')
		for node in xmltools:
			tool_name=node.getAttribute('name')
			wpdata,fidata,dirdata,headdata,juicydata,themedata = [],[],[],[],[],[]
			pcdata = False
			############## wordpatterns ###################
			wplist=node.getElementsByTagName('wordpatterns')
			for wp in wplist: wpdata = wp.firstChild.data
			if wpdata is not None: wpdata = wpdata.replace('\n','').replace('\t','').split(',')
			############### files #######################
			filelist=node.getElementsByTagName('files')
			for fi in filelist: fidata = fi.firstChild.data
			if fidata is not None: fidata = fidata.replace('\n','').replace('\t','').split(',')
			############### dirs ########################
			dirlist=node.getElementsByTagName('directories')
			for di in dirlist: dirdata = di.firstChild.data
			if dirdata is not None: dirdata = dirdata.replace('\n','').replace('\t','').split(',')
			############# headers #######################
			headlist=node.getElementsByTagName('headers')
			for hi in headlist: headdata = hi.firstChild.data
			if headdata is not None: headdata = headdata.replace('\n','').replace('\t','').split(',')
			############# juicyfiles #######################
			jflist=node.getElementsByTagName('juicyfiles')
			for jf in jflist: juicydata = jf.firstChild.data
			if juicydata is not None: juicydata = juicydata.replace('\n','').replace('\t','').split(',')
			############# themes #######################
			themelist=node.getElementsByTagName('themes')
			for th in themelist: themedata = th.firstChild.data
			if themedata is not None and len(themedata)>0:
				themedata = themedata.replace('\n','').replace('\t','').split(',')
			############# postcrawling #######################
			pclist=node.getElementsByTagName('postcrawl')
			for pc in pclist: pcdata = pc.firstChild.data
			if pcdata is not None:
				pcdata = pcdata.replace('\n','').replace('\t','')
				if pcdata == "True": pcdata = True
				else: pcdata = False
			sw[tool_name] = [wpdata,fidata,dirdata,headdata,juicydata,themedata,pcdata]
		#print('DEBUG swcontroller')
		for skey in sw.keys():
			print('\n{'+skey+':')
			for sk_elem in sw[skey]:
				print(sk_elem)
			print('}')
		return sw
		
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
		extres = []
		for tool in self.tools:
			if tool.hasDetections():
				extr = tool.launchTool()
				if extr is not None:
					extres.append(extr)
		return extres
		
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
				#temp+='\n'+tool.getResults()
				#temp = [tool.name]+tool.getResults()
				temp.append([tool.name]+tool.getResults())
		return temp
	
	# postcrawling, aqui obtengo los directorios no comunes y consulto los archivos default
	# solo se hace para los modulos que tuvieron detecciones
	def postCrawling(self):
		for tool in self.tools:
			if tool.hasDetections():
				#print "postcrawling with -> "+tool.getName()
				"""
				Aqui debo guardar el resultado de la llamada al modulo postcrawling
				Esta llamada es dinamica, por lo que puede regresar:
					nombre, listaderecursos
					nombre, cmsroot
				"""
				tmpres = tool.postCrawling()
				detectorname = tmpres[0]
				resourceslst = tmpres[1]
				cmsroot = None
				if len(tmpres)>2:
					cmsroot =  tmpres[2]
				#print "\nEn SWController@Postcrawling\n%s\n%s" % (tmpres[0],tmpres[1])
				#print "len de tmpres",len(tmpres)
				if cmsroot is not None: print "cmsroot -> ",cmsroot
				self.vulncontroller.setResources(detectorname,resourceslst,cmsroot)
				
			
	# Regresa una lista con los resultados de las herramientas externas
	"""
	def externalResults(self):
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
		return 'Software detection modules'+temp+'\n'

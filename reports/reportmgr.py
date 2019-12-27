#La estructura basica d	e un bloque de reporte es una lista
#El primer elemento de esta lista el nombre de los elementos o del detector
#ejemplo: mailscanner
#Los demas elementos son las detecciones, ie: [mailscan,mail1,mail2...mailn]
#Entonces puedo tratar al nombre del detector (elemento) de un modo distinto

#El segundo metodo recibe 2 cadenas, nombredeladeteccion,resultado
import os.path
#import html
from reports.reporthtml  import *		# reportes
from reports.reporttxt  import *		# reportes
from reports.reportxml  import *		# reportes
class reportmgr:
	
	def __init__(self,domain,fname,formats='txt,html',template="/base.css"):
		self.domain = domain
		#self.fname = fname
		# new
		self.formats = formats
		self.reports = []
		self.initObjects()
		
	def initObjects(self):
		self.formats = self.formats.split(',')
		if 'txt' in self.formats:
			rtxt = reportetxt(self.domain,self.domain)
			self.reports.append(rtxt)
		if 'html' in self.formats:
			rhtml = reporte(self.domain,self.domain)
			self.reports.append(rhtml)
		if 'xml' in self.formats:
			rxml = reportexml(self.domain,self.domain)
			self.reports.append(rxml)
			
	"""	
	def sitemap(self,reslist):
		for rp in self.reports:
			rp.sitemap(reslist)
			
	def sitemapXML(self,reslist):
		for rp in self.reports:
			rp.sitemapXML(reslist)
	"""
	
	############################################
	def sitemap(self,mapobj):
		for rp in self.reports:
			rp.sitemap(mapobj)
			
	def sitemapXML(self,mapobj):
		for rp in self.reports:
			rp.sitemapXML(mapobj)
			
	#############################################			
	def fromForms(self,formres):
		for rp in self.reports:
			rp.fromForms(formres)

	'''
		reslist: 	recursos a reportar (lineas de texto)
		tolinks:	booleano para indicar si transformar las lineas a enlaces
					Falso por defecto
	'''
	#def fromList(self,reslist):
	# La bandera tolinks sirve para especificar si los elementos pasados 
	# como parametros deben convertirse a enlaces html
	# la bandera extresult define si los resultados seran puestos en un bloque 
	# de codigo
	def fromList(self,reslist,tolinks=False,extresults=False):
		for rp in self.reports:
			rp.fromList(reslist,tolinks,extresults)
	
	def fromResources(self,resources):
		for rp in self.reports:
			rp.fromResources(resources)
			
	# Escribe el numero de pestanias utilizadas en el reporte, esto es para poder utilizar el cambio de los tabs
	def writeCSSX(self):
		for rp in self.reports:
			rp.writeCSSX()
			
	def finish(self):
		for rp in self.reports:
			rp.finish()

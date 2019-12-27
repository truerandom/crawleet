#La estructura basica d	e un bloque de reporte es una lista
#El primer elemento de esta lista el nombre de los elementos o del detector
#ejemplo: mailscanner
#Los demas elementos son las detecciones, ie: [mailscan,mail1,mail2...mailn]
#Entonces puedo tratar al nombre del detector (elemento) de un modo distinto

#El segundo metodo recibe 2 cadenas, nombredeladeteccion,resultado
import os.path
#import html
import cgi
class reportetxt:
	
	def __init__(self,domain,fname,template="/base.css"):
		self.domain = domain
		self.fname = fname+'.txt'
		self.template = template
		# Variable html
		self.code = ""
		self.scriptlibrary = ""
		# Agrego el codigo css en el header
		self.header1 = ""
		self.header2 = ''
		# Variable para el css
		self.css = ''
		self.radios = ""
		self.uls = ""
		self.content = ''
		self.footer = ""
		self.numelems = 0

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
		name = reslist[0]
		#print "name -> ",name
		#self.content+='\n\n%s' % (name)
		self.content+='\n\n'+'#'*60+'\n%s'% (name)+'\n'+'#'*60
		for r in reslist[1:]:
			self.content+='\n%s'%r
			#print r
		self.numelems+=1

	"""
	def sitemap(self,reslist):
		name = reslist[0]
		#self.content+='\n\n%s' % (name)
		self.content+='\n\n'+'#'*60+'\n%s'% (name)+'\n'+'#'*60
		# creo la tabla
		for r in reslist[1:]:
			self.content+='\n%s' % (r)
	"""
	
	# nuevo
	"""
	def sitemapXML(self,reslist):
		pass
	"""
	
	#############################################################
	def sitemap(self,mapobj):
		name = 'sitemap'
		#self.content+='\n\n%s' % (name)
		self.content+='\n\n'+'#'*60+'\n%s'% (name)+'\n'+'#'*60
		# creo la tabla
		reslist = mapobj.getMap()
		for r in reslist:
			self.content+='\n%s' % (r)
	
	def sitemapXML(self,mapobj): pass
	#############################################################	
	
	def fromResources(self,resources):
		name = "Resources"
		#self.content+='\n\n%s' % (name)
		self.content+='\n\n'+'#'*60+'\n%s'% (name)+'\n'+'#'*60
		for r in resources:
			self.content+='\n\n%s' % (r.getUrl())
			if r.hasForms():
				for f in r.getForms():
					self.content+='\nForm: %s' % f.action
		self.numelems+=1
	
	def writeCSSX(self): pass
		
	def fromForms(self,formres):
		name = "Forms"
		#self.content+='\n\n%s' % (name)
		self.content+='\n\n'+'#'*60+'\n%s'% (name)+'\n'+'#'*60
		for r in formres:
			self.content+='\n\n%s' % (r.getPath())
			if r.getName() is not None and r.getName() !='':
				self.content+='\n%s' % r.getName()
			if r.method is not None:
				self.content+='\n\t%s' % r.method
			for ctl in r.controls:
				self.content+='\n\t'+cgi.escape('%s'%ctl)
		self.numelems+=1
		
	def finish(self):
		f = open(self.fname, 'w')
		f.write(self.content)

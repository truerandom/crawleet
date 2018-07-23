#La estructura basica d	e un bloque de reporte es una lista
#El primer elemento de esta lista el nombre de los elementos o del detector
#ejemplo: mailscanner
#Los demas elementos son las detecciones, ie: [mailscan,mail1,mail2...mailn]
#Entonces puedo tratar al nombre del detector (elemento) de un modo distinto

#El segundo metodo recibe 2 cadenas, nombredeladeteccion,resultado
import os.path
#import html
import re
import cgi
class reportexml:
	
	def __init__(self,domain,fname,template="/base.css"):
		self.domain = domain
		self.fname = fname+'.xml'
		# Variable html
		# Agrego el codigo css en el header
		self.header = '<Reporte>'
		self.content = ''
		self.footer = '\n</Reporte>'
		self.numelems = 0

	'''
		reslist: 	recursos a reportar (lineas de texto)
		tolinks:	booleano para indicar si transformar las lineas a enlaces
					Falso por defecto
	'''
	# filtra caracteres no validos en xml
	def charfilter(self,input):
		if input:
			# unicode invalid characters
			RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
			u'|' + \
			u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
			(unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
			unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
			unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
			)
			input = re.sub(RE_XML_ILLEGAL, "", input)
			# ascii control characters
			input = re.sub(r"[\x01-\x1F\x7F]", "", input)
			return input

	#def fromList(self,reslist):
	# La bandera tolinks sirve para especificar si los elementos pasados 
	# como parametros deben convertirse a enlaces html
	# la bandera extresult define si los resultados seran puestos en un bloque 
	# de codigo
	def fromList(self,reslist,tolinks=False,extresults=False):
		name = reslist[0]
		tab = 4
		self.content+='\n'+' '*tab+'<%s>'% (name.replace(' ',''))
		for r in reslist[1:]:
			self.content+='\n'+' '*(tab*2)+'<data>%s</data>'%self.charfilter(cgi.escape('%s'%r))
			#print r
		self.numelems+=1
		self.content+='\n'+' '*tab+'</%s>'% (name.replace(' ',''))

	def sitemap(self,reslist):
		pass
			
	# nuevo
	def sitemapXML(self,reslist):
		tab = 4
		self.content+='\n'+' '*tab+'<sitemap>'
		for r in reslist:
			self.content+='\n'+' '*(tab*2)+'%s'%r
		self.content+='\n'+' '*tab+'</sitemap>'
	
	#########################################################
	def sitemapexp(self,mapobj):
		pass
	
	def sitemapXMLexp(self,mapobj):
		tab = 4
		reslist = mapobj.getXML().splitlines()
		self.content+='\n'+' '*tab+'<sitemap>'
		for r in reslist:
			self.content+='\n'+' '*(tab*2)+'%s'%r
		self.content+='\n'+' '*tab+'</sitemap>'
	#########################################################
			
	def fromResources(self,resources): pass
	
	def writeCSSX(self): pass
		
	def fromForms(self,formres): pass
		
	def finish(self):
		f = open(self.fname, 'w')
		f.write(self.header)
		f.write(self.content)
		f.write(self.footer)

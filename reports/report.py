#La estructura basica d	e un bloque de reporte es una lista
#El primer elemento de esta lista el nombre de los elementos o del detector
#ejemplo: mailscanner
#Los demas elementos son las detecciones, ie: [mailscan,mail1,mail2...mailn]
#Entonces puedo tratar al nombre del detector (elemento) de un modo distinto

#El segundo metodo recibe 2 cadenas, nombredeladeteccion,resultado
########################## REPORTE HTML ###########################
import os.path
#import html
import cgi

class reporte:
	
	def __init__(self,domain,fname,template="/base.css"):
		self.domain = domain
		self.fname = fname+'.html'
		self.template = template
		# Variable html
		self.code = ""
		self.scriptlibrary = """
		<link rel="stylesheet" href="%s">
		<script src="%s"></script>
		<script type='text/javascript'>%s</script>
		""" % ('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.2.0/styles/default.min.css',
		'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.2.0/highlight.min.js',
		'hljs.initHighlightingOnLoad();')
		# Agrego el codigo css en el header
		self.header1 = """
		<html>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width">
		<title>%s</title>%s\n<style>\n""" % (self.domain,self.scriptlibrary)
		'''
		self.header1 = """
		<html>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width">
		<title>%s</title>\n<style>\n""" % (self.domain)
		'''
		self.header2 = '\n</style>\n</head>\n\n<body>\n<h1>%s</h1>\n<div class="tabs">' % (self.domain)
		# Variable para el css
		self.css = ''
		self.radios = ""
		self.uls = "\n<ul>"
		self.content = '\n<div class="content">'
		self.footer = "</div></div>\n</body>\n</html>"
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
		# reporte txt
		#print '\n',name
		# css management
		if self.numelems == 3 :
			#self.radios+='\n<input type="radio" id="tab%s" name="tab-control" checked>' % (self.numelems) 
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control" checked>' % (self.numelems) # tab3 como default 
		else: 
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control">' % (self.numelems) 
		# css management
		self.uls+='\n<li title="%s"><label for="tab%s" role="button"><br><span>%s</span></label></li>' % (name,self.numelems,name)
		self.content+='\n<section>\n<h2>%s</h2>' % (name)
		# bloque de codigo
		if extresults:
			self.content+='\n<pre>\n\t<code class="sh">\n'
		for r in reslist[1:]:
			if tolinks:
				self.content+='<p><a href="%s">%s</a>' % (r,r)
			else:
				self.content+='<p>%s' % (r)
			# reporte txt
			#print r
		if extresults:
			self.content+='\n</code>\n\t</pre>'
		self.numelems+=1
		self.content+='</section>'

	#############################################################
	def sitemapexp(self,mapobj):
		name = 'sitemap'
		# reporte txt
		#print '\n',name
		if self.numelems == 0 :
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control" checked>' % (self.numelems) 
		else: 
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control">' % (self.numelems) 
		self.uls+='\n<li title="%s"><label for="tab%s" role="button"><br><span>%s</span></label></li>' % (name,self.numelems,name)
		self.content+='\n<section>\n<h2>%s</h2>' % (name)
		# creo la tabla
		self.content+='\n<table>\n<tr>'
		self.content+='\n<td>'
		# Agrego el sitemap linea a linea
		self.content+='\n<pre>\n\t<code>'
		reslist = mapobj.getMap()
		urllist = mapobj.getAbsUrls()
		#for r in reslist:
		#	self.content+='<p>%s' % (r)
		for i in range(0,len(reslist)):
			self.content+='<p><a href="%s">%s</a>' % (urllist[i],reslist[i])
			# reporte txt
			#print r
		self.content+='\n<p>\n\t</code>\n</pre>'
		self.content+='\n</td>'
		# chanfle hace falta pasar la imagen domain.jpg
		# la clase htext tiene en el css ocultar el texto de relleno
		# <pre><code><img src="becarios.unam.mx.jpg"></pre></code>
		self.content+='\n<td class="htext"><pre><code><img src="%s.jpg"></pre></code>' % (self.domain)
		for i in range(0,len(reslist)-10):
			self.content+='\n<p>.</p>'
		self.numelems+=1
		self.content+='\n</td></tr></table>'
		self.content+='</section>'
	
	def sitemapXMLexp(self,mapobj):
		pass
	#############################################################
	
	def sitemap(self,reslist):
		name = reslist[0]
		# reporte txt
		#print '\n',name
		if self.numelems == 0 :
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control" checked>' % (self.numelems) 
		else: 
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control">' % (self.numelems) 
		self.uls+='\n<li title="%s"><label for="tab%s" role="button"><br><span>%s</span></label></li>' % (name,self.numelems,name)
		self.content+='\n<section>\n<h2>%s</h2>' % (name)
		# creo la tabla
		self.content+='\n<table>\n<tr>'
		self.content+='\n<td>'
		# Agrego el sitemap linea a linea
		self.content+='\n<pre>\n\t<code>'
		for r in reslist[1:]:
			self.content+='<p>%s' % (r)
			# reporte txt
			#print r
		self.content+='\n<p>\n\t</code>\n</pre>'
		self.content+='\n</td>'
		# chanfle hace falta pasar la imagen domain.jpg
		# la clase htext tiene en el css ocultar el texto de relleno
		# <pre><code><img src="becarios.unam.mx.jpg"></pre></code>
		self.content+='\n<td class="htext"><pre><code><img src="%s.jpg"></pre></code>' % (self.domain)
		for i in range(0,len(reslist)-10):
			self.content+='\n<p>.</p>'
		self.numelems+=1
		self.content+='\n</td></tr></table>'
		self.content+='</section>'
	
	# nuevo
	def sitemapXML(self,reslist):
		pass
		
	def fromResources(self,resources):
		name = "Resources"
		# reporte txt
		#print '\n',name
		if self.numelems == 0 :
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control" checked>' % (self.numelems) 
		else: 
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control">' % (self.numelems) 
		self.uls+='\n<li title="%s"><label for="tab%s" role="button"><br><span>%s</span></label></li>' % (name,self.numelems,name)
		#######
		self.content+='\n<section>\n<h2>%s</h2>' % (name)
		#for r in resources[1:]:
		for r in resources:
			self.content+='<p><a href="%s"><h3>%s</a></h3>' % (r.getUrl(),r.getUrl())
			# reporte txt
			#print '\n',r.getUrl()
			#self.content+='<p>Status: %s' % r.getStatus()
			if r.hasForms():
				for f in r.getForms():
					self.content+='<p>Form: %s' % f.action
					# reporte txt
					#print "Form: ",f.action
		self.numelems+=1
		self.content+='</section>'
		
	def fromForms(self,formres):
		#print "\n","*"*50,"FORM RES","\n"
		name = "Forms"
		# reporte txt
		#print '\n',name
		if self.numelems == 0 :
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control" checked>' % (self.numelems) 
		else: 
			self.radios+='\n<input type="radio" id="tab%s" name="tab-control">' % (self.numelems) 
		self.uls+='\n<li title="%s"><label for="tab%s" role="button"><br><span>%s</span></label></li>' % (name,self.numelems,name)
		#######
		#self.content+='\n<section>\n<h2>%s</h2>' % (name)
		self.content+='\n<section>\n<h2>%s</h2>' % (name)
		#for r in resources[1:]:
		for r in formres:
			#print type(r)
			#print r
			#print "Metodo con metodo %s atributo %s " % (r.getMethod(),r.method)
			self.content+='<p><a href="%s"><h3>%s</a></h3>' % (r.getPath(),r.getPath())
			# reporte txt
			#print '\n',r.getPath()
			if r.getName() is not None:
				self.content+='<p><h3>%s</h3>' % r.getName()
				# reporte txt
				#print r.getName()
			if r.method is not None:
				#print "Entre al if de method "
				#print r.method
				self.content+='<p> %s' % r.method
				# reporte txt
				#print '\t',r.method
			for ctl in r.controls:
				self.content+='<p>'+cgi.escape('%s'%ctl)
				# reporte txt
				#print '\t',ctl
		self.numelems+=1
		self.content+='</section>'
		
	# Escribe el numero de pestanias utilizadas en el reporte, esto es para poder utilizar el cambio de los tabs
	def writeCSSX(self):
		# Agrego el numero de pestanas al css
		for i in range(1,self.numelems+1):
			self.css+='\n.tabs input[name="tab-control"]:nth-of-type(%s):checked ~ ul > li:nth-child(%s) > label {cursor: default;color: #428BFF;}'%(i,i)
			self.css+='\n.tabs input[name="tab-control"]:nth-of-type(%s):checked ~ .content > section:nth-child(%s) {display: block;}'%(i,i)
		
	def finish(self):
		self.uls+='\n</ul>'
		try:
			fn = os.path.dirname(__file__)
			with open(fn+self.template) as basecss:
				self.css = basecss.read()
		except Exception as e:
			print 'Report error: ',e
		# Agrego los tabs
		self.writeCSSX()
		# Escribo el codigo html
		f = open(self.fname, 'w')
		f.write(self.header1)
		f.write(self.css)
		f.write(self.header2)
		f.write(self.radios)
		f.write(self.uls)
		f.write(self.content)
		f.write(self.footer)

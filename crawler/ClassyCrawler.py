import sys
import requests
import lxml.html
import re
import time
import collections
from anytree import *
import posixpath 
import cgi
from urlparse import urlparse
# clase para reportess
from reports.report  import *
from results.nodoresultado import *
from results.Formulario import *
from detection.swcontroller import *
from detection.swdetection import *
from detection.vulncontroller import *
from detection.vulndetection import *
from sitemap import test
from utils import parseurls
from utils import ubanner
from utils.bruteforcer import *	# chanfle
try:
	from colorama import init, Fore,Back, Style
except:
	pass
class ClassyCrawler:
	def __init__(self,req,reportex,url,depth,delay,bruteforce,backups,wordlist,runexternaltools,cfgfile,datadir,extensions,verbose,exclude,maxfiles=1000,color=False):
		self.banner = ubanner.getBanner()
		self.reportex = reportex			# modulo de reportes	
		self.url = url						# url
		self.color = color
		self.domain = self.getDomain(self.url)
		self.req = req						# objeto para realizar las peticiones
		self.depth = depth					# depth
		self.delay = delay					# delay between requests
		self.maxfiles = maxfiles			# maximum files to analize
		self.wordlist = wordlist			# wordlist to bruteforce
		self.exclude = exclude				# excluir archivos o directorios
		self.tovisit = collections.OrderedDict()
		self.visited = collections.OrderedDict()
		self.extlinks = []					# link externos del aplicativo
		self.flist = []						# links con archivos del aplicativo
		self.brokenlist = []				# links con archivos 404 o 500 del aplicativo
		self.visitedresources = []			# visited resources (objetos)
		self.cfgfile = cfgfile				# directorio de el archivo de cfg para exttool
		self.datadir = datadir				# directorio de data para las detecciones
		self.runexternaltools = runexternaltools	# ejecutar herramientas externas
		# detector de vulnerabilidades
		self.vulndetector = vulncontroller(cfgfile,req,self.color)
		# detector de software
		self.swdetector = swcontroller(cfgfile,self.datadir,req,self.vulndetector,self.color)		# archivod de configuracion de herramientas ext
		#################### BRUTEFORCER ##########################
		self.bruteforce = bruteforce	# variable para decidir si hacer bruteforce
		self.bforcer = bruteforcer(req,extensions,delay,verbose,wordlist)
		self.backups = backups	#search for currentfile backups
		self.directories = []
		self.interestingfiles = []
		self.puntuacion = 0
		self.verbose = verbose
		# formularios tab
		self.forms = []
		# cadena para el sitemap
		self.sitemap = ''
		
	# regresa la prioridad para este sitio:
	# se calcula usando
	# el numero de recursos visitados, archivos encontrados
	# y puntuacion regresada por los modulos de deteccion
	def getPriority(self):
		# defcore -> 100 
		# puntuacion = x%
		defscore = len(self.visitedresources)+len(self.flist)
		if defscore == 0: defscore = 1
		tscore = self.puntuacion / defscore
		# si tscore < 30: low : tscore< 80 : medium < tscore > high
		return tscore
		
	# define la base (subdominio) para hacer el crawl
	def getDomain(self,direccion):
		return direccion.split("//")[-1].split("/")[0].replace('www.','')
	
	def fixUrl(self,url):
		try:
			if url is not None:				
				parsed = urlparse(url)
				new_path = posixpath.normpath(parsed.path)
				cleaned = parsed._replace(path=new_path)
				cleanurl = cleaned.geturl()
				if url[-1] == '/':
					cleanurl+='/'
				if self.verbose:
					print 'Entre a fixUrl con %s ' % url
					#print 'Parsed %s ' % parsed
					print 'Cleaned %s ' % cleanurl
				return cleanurl
		except Exception as e:
			print "FixUrl Something wrong with %s "%url
			print e
			return None
    		
	# tupla que regresa:
	#	None si no es un archivo html
	#	(ishtml,code) 
	def isHTML(self,frequest):
		try:
			if frequest is not None:
				if 'html' in frequest.headers['content-type']:
					return (True,frequest.status_code)
				return (False,frequest.status_code)
			return None
		except:
			return None

	def getForms(self,code):
		try:
			pagesource = code
			# treeparser = 
			tree = lxml.html.fromstring(pagesource)
			formlist = []
			# Obtengo los formularios
			formularios = tree.xpath('.//form')
			for form in formularios:
				actform = Formulario('',form.action,form.method,[])
				actform.setAction(form.action)
				actform.setMethod(form.method)
				campos = []
				for f in form.inputs.keys():
					campos.append(form.inputs[f])
				actform.setControls(campos)
				formlist.append(actform)
			self.puntuacion = self.puntuacion+(len(formlist)*5)
			return formlist
		except:
			print "something wrong"
			return []
		
	# param: link
	# returns: si el link pasado es absoluto
	def isAbsolute(self,link):
		link = link.strip()
		linkpattern = '([A-Za-z0-9])+://'
		return re.match(linkpattern,link)

	# Regresa el prefijo del recurso ie url de url/recurso
	def getPreffix(self,baseurl):
		return baseurl.rsplit('/',1)[0]+'/'

	# Tomo la url actual, url .../recurso quito el recuro y hago la peticion
	# Tengo que identificar si hay listado de directorios, si es asi regreso True
	def directoryListing(self,url):
		dlistingstrings = ["<title>Index of","\[To Parent Directory\]"]
		url = self.getPreffix(url)
		if self.domain in self.getDomain(url):
			try:
				htmlcode = self.req.getHTMLCode(url)
			except Exception as e:
				print "Error@Crawler:directoryListing "+e
				htmlcode = None
			if htmlcode is not None and htmlcode.status_code < 300: 
				for dliststring in dlistingstrings:
					if len(re.findall(dliststring,htmlcode.text,re.IGNORECASE)) > 0:
						return True
			else:
				return False
		return False

	# bruteforce: recibe una url .../recurso quita el recurso y hace bruteforce
	def bruteForce(self,baseurl):
		try:
			filesfound = self.bforcer.directory(baseurl)
			return filesfound
		except Exception as e:
			print "Error in bruteforce -> ",e
			return None
			
	# Utilizar parseurl o test para arreglar esto
	def getLinks(self,code,actualpage):
		try:
			dom = lxml.html.fromstring(code)
			intlinks = []
			extlinks = []
			for linkx in dom.iterlinks():
				try:
					link = linkx[2]	# nuevo
					if self.isAbsolute(link):
						# si baseurl esta contenida en el link absoluto es un link interno
						if self.domain in self.getDomain(link) and self.getDomain(link).startswith(self.domain):
							intlinks.append(link.strip())
						else:
							if link.strip() not in self.extlinks:
								self.extlinks.append(link.strip())
					else:
						if self.verbose:
							print 'entre a normalize con %s ' % link
						newlink = parseurls.normalize(actualpage,link)
						intlinks.append(newlink)
				except Exception as e:
					print e
			# Aqui debo hacer el bruteforce de links
			if self.bruteforce == True:
				bres = self.bruteForce(actualpage)
				if bres is not None: intlinks.extend(bres)
			return (intlinks,extlinks)
		except:
			return ([],[])
		
	def addLinks(self,intlinks,nivel,pnode):
		for actlink in intlinks:
			# si los links encontrados no han sido visitados ni estan por, lo agrego
			actlink = self.fixUrl(actlink)
			if actlink is not None:
				actlink = parseurls.removeExtraSlashes(actlink)
				toexclude = False
				for ex in self.exclude:
					if ex in actlink:
						toexclude = True
				if not self.visited.has_key(actlink) and not self.tovisit.has_key(actlink) and not toexclude:
					self.tovisit[actlink]=nodoresultado(actlink,pnode.getUrl(),nivel+1,pnode)
					self.puntuacion = self.puntuacion + 1
				
	def crawl(self):
		startpage = self.url
		self.tovisit = collections.OrderedDict()
		self.tovisit[startpage.strip()] = nodoresultado(startpage.strip(),'',0)
		externallinks = []
		# lista de archivos encontrados
		self.visited=collections.OrderedDict()
		i = 0
		while len(self.tovisit)>0 and len(self.visited) < self.maxfiles:
			if self.verbose:
				if self.color:
					try:
						print (Fore.GREEN+"\nVisited elems: "+Fore.BLUE+len(self.visited)+Style.RESET_ALL)
					except:
						print "Visited elems: ",len(self.visited)
				else:
					print "Visited elems: ",len(self.visited)
			# 'url':nodores
			elem = self.tovisit.items()[0][1]
			actualpage = elem.getUrl()
			nivel = elem.getNivel()
			# elimino el elemento de tovisit
			del self.tovisit[actualpage]
			if self.color:
				try:
					print (Fore.GREEN+"\nRecurso: "+Fore.BLUE+actualpage+Style.RESET_ALL)
					print (Fore.GREEN+"Current level: "+Fore.BLUE+str(nivel)+Style.RESET_ALL)
					print (Fore.GREEN+"Remaining elems: "+Fore.BLUE+str(len(self.tovisit))+Style.RESET_ALL)
				except:
					print "\nRecurso: ",actualpage			
					print 'current level: ',nivel
					print 'remaining elements: ',len(self.tovisit)
			else:
				print "\nRecurso: ",actualpage			
				print 'current level: ',nivel
				print 'remaining elements: ',len(self.tovisit)
			# Hacemos el delay
			time.sleep(self.delay)
			# Hago una peticion head
			actreq = self.req.getHeadRequest(actualpage)
			# Determino si es un recurso html (con los headers)
			status = self.isHTML(actreq)
			#print 'Status %s ' % status
			self.visited[actualpage]=elem
			if status is not None and status[0] == True:
				# Analizo por posibles vulnerabilidades en el recurso
				self.vulndetector.fromFilename(actualpage)
				# Analiza los headers del recurso para hacer fingerprint
				self.swdetector.fromHeaders(actreq.headers,actualpage)
				try: elem.setStatus(actreq.status_code)
				except Exception as e:	# error en el servidor
					status[1] = 500
				# Obtenemos el codigo fuente si es un codigo < 400 
				if status[1] < 400:
					try: actualcode = self.req.getHTMLCode(actualpage).text
					except Exception: actualcode = None
					if actualcode is not None:
						# detecto elemetos del codigo fuente
						self.swdetector.fromCode(actualcode,actualpage)
						# Obtengo los links internos y externos del codigo
						# Debo pasar la url de este nodo, para que sus links
						# hijos relativos lo tengan
						links = self.getLinks(actualcode,actualpage)
						if self.verbose:
							print 'Links'
							print links
						intlinks = links[0]
						# agrego los links al recurso
						elem.setLinks(intlinks)
						# obtengo los formularios
						formularios = self.getForms(actualcode)
						elem.setForms(formularios)
						# agrego este recurso a la lista de recursos visitados
						self.visitedresources.append(elem)
						if elem.hasForms() == True: print "Tiene formularios"
						# Verifico si hay listado habilitado
						dirlisting = self.directoryListing(actualpage)
						if dirlisting:
							print "Directory listing enabled"
							actualdir = self.getPreffix(actualpage)
							if self.verbose:
								print 'dir found ',actualdir
							if actualdir not in self.directories:
								self.directories.append(actualdir)
								intlinks.append(actualdir)
						# bruteforce
						if self.backups:
							# el padre de estos nodos debe ser el actual o el padre(actual)?
							bkplinks = self.bforcer.thisFile(actualpage)
							if len(bkplinks)>0:
								self.addLinks(bkplinks,nivel,elem)
						if self.bruteforce:
							blinks = self.bruteForce(actualpage)
							if blinks is not None and len(blinks) > 0:
								if nivel+1 < self.depth:
									self.addLinks(blinks,nivel,elem)
						# Si el nivel siguiente no es el limite los agregamos
						if nivel+1 < self.depth: 
							self.addLinks(intlinks,nivel,elem)
					else:
						print "Something wrong with ",actualpage
				# encontre un 400 o 500
				else:
						print "Broken link: ",actualpage
						if actualpage not in self.flist:
							self.brokenlist.append(actualpage)
						self.swdetector.fromFilename(actualpage)
			else:
				print "File found: ",actualpage
				# Detect from filename
				print "Detecting from filename -> ",actualpage
				self.swdetector.fromFilename(actualpage)
				self.flist.append(elem)
				# optimizar
				dirlisting = self.directoryListing(actualpage)
				if dirlisting:
						print "Directory Listing enabled" 
						if self.verbose:
							print 'current level ',nivel
						actualdir = self.getPreffix(actualpage)
						if actualdir not in self.directories:
							self.directories.append(actualdir)	
							if nivel+1 < self.depth: 
								self.addLinks([actualdir],nivel,elem)
				if self.backups:
					# el padre de estos nodos debe ser el actual o el padre(actual)?
					bkplinks = self.bforcer.thisFile(actualpage)
					if bkplinks is not None and len(bkplinks)>0:
						self.addLinks(bkplinks,nivel,elem)
				if self.bruteforce == True:
					blinks = self.bruteForce(actualpage)
					if blinks is not None and len(blinks) > 0:
						if nivel+1 < self.depth:
							self.addLinks(blinks,nivel,elem)
		####################### FIN CRAWLING ###########################
		
		####################### IMPRESION CONSOLA ######################
		####################### Recursos ###############################
		if self.color:
			try: print (Fore.BLUE+"\n"+"*"*100+"\nResources\n"+"*"*100+"\n"+Style.RESET_ALL)				
			except: print "*"*100+"\nResources\n","*"*100,"\n"
		else:
			print "*"*100+"\nResources\n","*"*100,"\n"
		for res in self.visitedresources:
			print "Url: ",res.url
			if res.hasForms() == True:
				for fx in res.getForms(): 
					if fx.action is not None:
						print '\tForm: ',fx.action
		####################### Links rotos ###############################
		if self.color:
			try: print (Fore.BLUE+"\nBroken Links: \n"+Style.RESET_ALL+"\n".join(self.brokenlist))
			except: print "\nBroken Links: \n","\n".join(self.brokenlist)
		else:
			print "\nBroken Links: \n","\n".join(self.brokenlist)
		####################### Files found ###############################
		if self.color:
			try:print (Fore.BLUE+"\nFiles found: \n"+Style.RESET_ALL)
			except: print "\nFiles found:\n"
		else:
			print "\nFiles found:\n"
		for f in self.flist:
			print f.getUrl()
		####################### Ext Links ###############################
		if self.color:
			try: print (Fore.BLUE+"\nExternal links: \n"+Style.RESET_ALL+"\n".join(self.extlinks))
			except: print "\nExternal links:\n","\n".join(self.extlinks)
		else:
			print "\nExternal links:\n","\n".join(self.extlinks)
		####################### DirListing ###############################
		if self.color:
			try: print (Fore.BLUE+"\nDir Listing: \n"+Style.RESET_ALL+"\n".join(sorted(set(self.directories))))
			except: print "\nDirectory Listing:\n","\n".join(sorted(set(self.directories)))
		else:
			print "\nDirectory Listing:\n","\n".join(sorted(set(self.directories)))
		####################### Raiz ##################################
		try: nraiz = self.visitedresources[0]
		except Exception as e: print "no visited elements: %s " % e
		####################### Resultados modulos #####################
		for res in self.swdetector.results():
			if self.color:
				try: print (Fore.BLUE+res[0]+"\n"+Style.RESET_ALL+"\n".join(res[1:]))
				except: print '\n','\n'.join(res)
			else:
				print '\n','\n'.join(res)
		####################### POST DETECTION #######################
		self.swdetector.postCrawling()
		##################### ExtResults I ########################
		extresults = []
		if self.runexternaltools:
			# obtenemos los resultados de las herramientas externas
			print "running external tools"
			extresults = self.swdetector.runExtTools()
		######################### PUNTUACION ##########################
		self.puntuacion+= len(self.directories)
		self.puntuacion+= self.swdetector.getPuntuation()
		######################### PRIORIDAD ###########################
		priority = self.getPriority()
		#print priority
		###############################################################
		###########			INICIO DE REPORTES  ###########
		###############################################################
		# ESTADISTICAS
		estadisticas = ['Puntuation: '+str(self.puntuacion),
						'Priority: ',str(priority).rstrip(),
						'Resources: '+str(len(self.visitedresources)),
						'Broken Links: '+str(len(self.brokenlist)),
						'Files found: '+str(len(self.flist)).rstrip(),
						'External links: '+str(len(self.extlinks)),
						'Directory listing: '+str(len(self.directories))]
		# Lista para los resultados de los modulos de deteccion
		detectionres = [] 
		for res in self.swdetector.results():
			# Tomo los resultados del detector
			tmp = res
			detectionres.append(tmp)
			# Agrego las detecciones para las estadisticas
			estadisticas.append(tmp[0]+': '+str(len(tmp[1:])))
		self.reportex.fromList(['statistics']+estadisticas)
		######################### DETALLES #############################
		if len(self.directories) > 0:
			self.reportex.fromList(['directory listing']+sorted(self.directories),True)
		##########################Files#################################
		filelist = []
		for f in self.flist: filelist.append(f.getUrl())
		if len(filelist)>0:
			self.reportex.fromList(['files']+sorted(filelist),True)
		if len(self.brokenlist)>0:
			self.reportex.fromList(['broken links']+sorted(self.brokenlist))
		if len(self.extlinks)>0:
			self.reportex.fromList(['external links']+sorted(self.extlinks),True)
		# Genera los reportes para los hallazgos de los modulos de deteccion
		for detected in detectionres:
			self.reportex.fromList(detected)
			print "\nDEBUG\n".join(detected)
		###################### RESOURCES ########################
		self.reportex.fromResources(self.visitedresources)
		print "\nPuntuacion: ",self.puntuacion
		###########################Formularios##########################
		unida = parseurls.getDomain(self.url)
		if self.url.endswith('/'): unida+='/'
		listforms = [] 	# unique forms
		addedforms = []	# forms to report
		for res in self.visitedresources:
			actresurl = res.getUrl()
			if res.hasForms():
				for f in res.getForms():
					actaction = f.getAction()
					actpath = parseurls.normalize(actresurl,actaction)
					f.setPath(actpath)
					if actpath not in addedforms:
						addedforms.append(actpath)
						listforms.append(f)
		#listforms es una lista de objetos formulario
		if self.color:
			try: print (Fore.BLUE+'FORMS'+Style.RESET_ALL)
			except: print '\n','*'*40,'FORMS','*'*40
		else:
			print '\n','*'*40,'FORMS','*'*40
		for form in listforms: print form
		if len(listforms)> 0:
			self.reportex.fromForms(listforms)
		#################### VULNERABILITIES ###########################
		vulnres = []
		for res in self.vulndetector.results():
			# Tomo los resultados del detector
			tmp = res
			print 'DEBUG VULN \n',tmp
			vulnres.append(tmp)
		for detected in vulnres:
			print 'DEBUG DETECTED\n',detected
			self.reportex.fromList(detected)
		#################### REPORT EXTRESULTS #########################
		if self.color:
			try: print (Fore.BLUE+"External Results"+Style.RESET_ALL)
			except: print "External Results"
		else:
			print "External Results"
		for extres in extresults: 
			print extres
			# Si es un resultado externo, ahref = False, Extres=True
			self.reportex.fromList(extres.splitlines(),False,True)
		###################GENERACION XML Y SITEMAP####################
		# sitemap
		smapobj = test.parseResources(self.domain,unida,self.visitedresources+self.flist,listforms)
		#print '\n'.join(smap2[0])
		print '\n'.join(smapobj.getMap()) # sitemap[0] = sitemap,ligas
		self.reportex.sitemapexp(smapobj)
		self.reportex.sitemapXMLexp(smapobj)
		################################################################
		############			FIN DE REPORTES		########
		################################################################

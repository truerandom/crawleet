#import html
import re
#import urllib
from urlparse import urljoin
'''
Metodos auxiliares para el tratamiento de urls
Utilizado en la union de recursos y la union de sus formularios
'''
'''
Sea recurl = http:recpath/recfinal la url de la paguna actual
	ie recfinal es lo que esta al final de la ultima diagonal
Action url es la url que tiene el formulario ie donde se enviaran los datos
recurl y action url
Casos de action url:
	[A] es absoluta:
		path = actionurl
	[B] No es absoluta
		[1] acturl no tiene (..) ie acturl en el mismo nivel o bajo que recurl
			[1]acturl tiene /s"
				[1]acturl empieza con /:
					NEW
						Esto implica que es una ruta absoluta desde el dominio??
						tomo el dominio y le pego la actionurl
					OLD
						quito recfinal de recurl
						quito la primera diagonal de acturl=:: acturlfix
						pego estas dos
				[2]actual no empieza:
					quito recfinal de recurl
					return recurl+acturl
			[2]	acturl no /s (tiene esta en el mismo nivel):
					quito recfinal
					pego a recurl acturl	
				Se quita recfinal y se pega acturl
		[2] acturl tiene .. ie esta en niveles superiores ie acturl 
			Remuevo el recfinal de recurl
			Ie acturl es de la forma ../../algo
			Tengo que contar el numero de dos puntos en acturl
			Este es el numero de directorios a quitar de recurl
			Despues tengo que quitar el numero de directorios ie el 
			numero de dos puntos encontrados de izq a derecha
			en recurl =:: recurlfix
			Luego concateno el recfinal de acturl a recurlfix
			y regreso esto
'''

#Funcion que regresa http[s]://dominio de una url sin la diagonal al final
def getDomain(url):
	proto = "".join(url.split('//')[0])+'//'
	domain = "".join(url.split('//')[1]).split('/')[0]
	return proto+domain

# regresa solo el dominio sin protocolo
def domainOnly(url):
	proto = "".join(url.split('//')[0])+'//'
	domain = "".join(url.split('//')[1]).split('/')[0]
	return domain
	
# Obtiene todos los directorios basados en los recursos encontrados
def getDirectories(urls):
	#print "debug: entre a get directories urls[0] "+urls[0]
	#print 'debug: fullurls ',urls
	dirs = []
	domain = ''
	if len(urls)>0:
		domain = getDomain(urls[0])
	for url in urls:
		#print url
		try:
			if getDomain(url).startswith(domain):
				actdir = quitaRecFinal(url)
				if actdir not in dirs and actdir.startswith(domain):
					dirs.append(actdir)
		except Exception as e:
			print "Error@getDirectories url %s e %s " % (url,e)
	#print dirs
	#print "sali de getdirectories"
	return dirs

# Funcion que regresa dirs distintos a los default en el cms
# paso el dominio, la lista de directorios a analizar y los dirs default
def uncommonDirectories(dirs,defdirs):
	uncommondirs = []
	domain = ''
	if len(dirs)>0:
		domain = getDomain(dirs[0])
	for dir in dirs:
		toadd = True
		for defd in defdirs:
			if dir.startswith(domain+defd):
				toadd = False
		if toadd:
			uncommondirs.append(dir)
	return uncommondirs
	
# recurl:- url del padre ie pagina que llama al formulario
# actionurl ruta del formulario (puede ser relativa).
def normalize(recurl,actionurl):
	try:
		if esAbsoluta(actionurl):
			return actionurl
		return urljoin(recurl,actionurl)
	except Exception as e:
		print 'error@normalize with recurl %s acurl %s ' % (recurl,actionurl)
		return None
	"""
	try:
		recurl = quitaRecFinal(recurl)
		if esAbsoluta(actionurl):	# CASO A
			print 'Debug @normalize %s es absoluta ' % actionurl
			return actionurl
		# No es absoluta caso B
		print 'Debug @normalize %s no es absoluta ' % actionurl
		pts = cuentaSubcadenas(actionurl,'..')
		if pts == 0:	# Caso B.1
			#print 'Caso B.1'
			if cuentaSubcadenas(actionurl,'/') > 0: # B.1.1
				if actionurl.startswith('/'):	# B.1.1.1
					#return recurl+actionurl[1:]
					print 'Caso B.1.1'
					return getDomain(recurl)+actionurl
				else:						# B.1.1.2
					print 'Caso B.1.1.2'
					return recurl+actionurl
			else:
				print 'Caso B.1.2'
				return recurl+actionurl		#B.1.2
		else:
			print 'Caso B.2'
			recurl = quitaDiagonales(recurl,pts)	# B.2
			return recurl+getRecFinal(actionurl)
	except Exception as e:
		print "Error @normalize\n%s recurl %s actionurl %s "%(e,recurl,actionurl)
	"""
def removeExtraSlashes(acturl):
	slashlist = acturl.split('//')
	endslash = ''
	try:
		proto = ''.join(slashlist[0])+ '//'
		path = acturl[len(proto):]
		pattern = '/{2,}'
		p = re.sub(pattern,'/',path)
		return proto+p+endslash
	except Exception as e:
		print "error@removeSlashes"
		return acturl
		
# True si la url es absoluta
def esAbsoluta(recurl):
	linkpattern = '([A-Za-z0-9])+://'
	if re.match(linkpattern,recurl) is not None:
		return True
	return False
	
# recurl:= http[s]://domain/dir1/dir2/dirn/rec
# regresa http[s]://domain/dir1/dir2/dirn/
def quitaRecFinal(cad):
	lcad = len(cad)
	for i in reversed(range(lcad)):
		if cad[i] == '/':
			return cad[:i+1]

# Sea url:= http://dom/dir1/dir2/recfinal
# regresa recfinal
def getRecFinal(cad):
	#print 'entre a recfinal con cad -> ',cad
	lcad = len(cad)
	for i in reversed(range(lcad)):
		if cad[i] == '/':
			return cad[i+1:]
			
# quita una diagonal y todas las letras hasta encontrar otra diagonal
# de derecha a izq. ie si urL:= ://path1/path2/path3/
# el resultado de aplicar este metodo es ://path1/path2/
def quitaDiagonal(cad):
	lcad = len(cad)
	encontrada = False
	for i in reversed(range(lcad)):
		# encontre la diagonal limite izq
		if cad[i] == '/':
			if encontrada == True:
				#print cad[:i+1]
				return cad[:i+1]
			else:
				encontrada = True
			
# quita n diagonales (incluyendo lo que haya en medio de 2 diagonales )
# de der a izq y regresa el resultado
def quitaDiagonales(recurl,num):
	#print "Quitando %s diagonales de %s " % (num,recurl)
	recurlx = recurl
	for i in range(0,num):
		recurlx = quitaDiagonal(recurlx)
	#print "Result %s "%recurlx
	return recurlx

# Regresa el numero de repiticiones de una subcadena en la cadena principal
def cuentaSubcadenas(recurl,subcad):
	return recurl.count(subcad)

# Genera posibles nombres para archivos de respaldo del recurso pasado como parametro
def getBackupNames(resname):
	#print "entre a backupnames [%s] " % resname
	if len(resname) > 0:
		exts = [
			"~%s" % resname,
			"%s~" % resname,
			"%s.back" % resname,
			"%s.bkp" % resname,
			"%s.backup" % resname,
			"%s.tmp" % resname,
			"%s.res" % resname
		]
		return exts
	return []
	
'''
	Dirs es un diccionario donde la llave es la carpeta y el valor es el
	nivel de profundidad en el cms de dicha carpeta
	Por ejemplo si el cms es wordpress y la carpeta wp-admin
	en dirs tenemos:
		dirs['wp-admin'] = 1
	Entonces si en los directorios se encuentra wp-admin la raiz esta
	un nivel mas arriba por lo que a la ruta donde se encontro wp-admin
	debe quitarsele un nivel mas
'''
def getCMSRoot(reslist,defdirs):
	#print "entre a @getCMSROOT"
	founddirs = getDirectories(reslist)
	#print "len found dirs %s"%len(founddirs)
	#print "FOUND DIRS ",founddirs
	#print "DEFDIRS ",defdirs.keys()
	for ddir in founddirs:
		for defdir in defdirs.keys():
			if defdir in ddir:
				try:
					#print 'found %s in %s level %s' % (defdir,ddir,defdirs[defdir])
					return getCMSRootX(ddir,defdir,defdirs[defdir])
				except Exception as e:
					return getCMSRootX(ddir,defdir,1)
				'''
				print 'found %s in %s level %s' % (defdir,ddir,defdirs[defdir])
				return getCMSRootX(ddir,defdir,defdirs[defdir])
				'''
# Metodo interno para CMSRoot quita level-1 diagonales de la url detectada
def getCMSRootX(baseurl,defdir,level):
	try:
		#print 'resultado de quitadiag ',quitaDiagonales(baseurl.split(defdir)[0],level-1)
		return quitaDiagonales(baseurl.split(defdir)[0],level-1)
	except Exception as e:
		print "Error @getCMSRoot: ",e
		return None


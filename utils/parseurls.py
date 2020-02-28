#import html
import re
#import urllib
from urlparse import urljoin

def get_extension(the_url):
	last_idx = the_url.rfind('.')
	if last_idx !=-1:
		ext = the_url[last_idx:]
		try:
			m = re.search("(\.[A-Za-z0-9]+)",the_url[last_idx:])
			return m.group()
		except Exception as e:
			return ""
	else:
		return ""
		
def getList(file_name):
	try:
		#print('parseurl.getList with %s' % file_name)
		#print(type(file_name))
		with open(file_name) as f:
			return f.read().splitlines()
	except Exception as e:
		print('error parseurl@getList')
		print(e)
		return []		
		
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
	founddirs = getDirectories(reslist)
	print('[i] getCMSRoot:')
	print('Resource list:')
	print(' '.join(reslist))
	#print('Default dirs:')
	tmp = [ '%s:%s' % (dkey,defdirs[dkey]) for dkey in defdirs.keys()]
	print(' '.join(tmp))
	print('found dirs: ')
	print('\n'.join(founddirs))
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
		
#[(url_resource,url?var_to_inject=placeholder&var2=val...&varn=valn)...(url_res,url_to_inject,var_name)]
def get_injection_points(url):
	new_url = re.sub('&+','&',url)
	# now we split with the token ?
	list_split_base_url = new_url.split('?')
	# el primer elemento del split es la base de la url
	# el elemento de la derecha son los parametros
	if len(list_split_base_url) < 2:
		return None
	else:
		# base_url = url_resource = http://dom/resource
		base_url = "%s?" % list_split_base_url[0]
		# url_vars_string = var1=val1&var2=val2&...&varn=valn
		url_vars_string = ''.join(list_split_base_url[1:])
		# [var1 = val1, var2=val2, ..., varn=valn]
		var_list = url_vars_string.split('&')
		#print('base_url: %s' % base_url)
		#print('url_vars: %s' % url_vars_string)
		injection_points = []
		for i in range(0,len(var_list)):
			var_info = var_list[i]
			var_name = var_info.split('=')[0]
			var_fixed = '%s={TO_REPLACE}' % var_name
			url_to_inject = '%s%s' % (base_url,'&'.join(var_list[0:i]+[var_fixed]+var_list[i+1:]))
			#injection_points.append(fixed_url)
			#url_resource,url?var_to_inject=placeholder&var2=val...&varn=valn
			injection_data = (base_url,url_to_inject,var_name)
			#print('injection_data')
			#print(injection_data)
			injection_points.append(injection_data)
		#print('injection_points: for %s ' % base_url)
		#print(injection_points)
		#print('\n'.join(injection_points))
		return injection_points

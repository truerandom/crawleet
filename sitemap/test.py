from anytree import *
from results.nodoresultado import *
from results.simplenode import *
from results.Formulario import *
from anytree.dotexport import RenderTreeGraph
from sitemap.mapobj import *
from utils import parseurls
#import html
import test
import sys
import cgi
# Genera el sitemap a partir de un nodo raiz
# El tipo de nodo es 
def sitemap(bnode):
	tmpsmap = []		# lista para el sitemap
	tmpabsurls = []		# lista para las urls absolutas
	for pre, fill, node in RenderTree(bnode):
		tmpmap = "%s%s" % (pre,node.getUrl())	#parte del smap
		tmpsmap.append(tmpmap)
		tmpabs = node.getFPath()				# urlasociada
		tmpabsurls.append(tmpabs)				
	return (tmpsmap,tmpabsurls)

# Aqui genero el xml
# Donde pre es el tamanio del separador entonces solo me fijo si se abre un nuevo nodo
# Debo de tener un contador para cerrar los recursos
def siteXML(bnode,forms=None,estadisticas=None):
	tmpx = ''
	preant=-1
	nums = 0
	# Longitud default para pre de anytree
	tab = 4
	########################## statistics ###########################
	if estadisticas is not None:
		tmpx+='\n'+' '*tab+'<Stats>'
		for stat in estadisticas:
			#tmpx+='\n'+' '*(tab*2)+'<stat>%s</stat>'%(html.escape(str(stat)))
			tmpx+='\n'+' '*(tab*2)+'<stat>%s</stat>'%(cgi.escape(str(stat)))
		tmpx+='\n'+' '*tab+'</Stats>'
	########################## statistics ###########################
	########################## Aqui paso los formularios ############
	if forms is not None:
		for form in forms:
			tmpx+='\n'+' '*tab+'<Form>'
			if form.getPath() is not None and form.getPath() !='':
				tmpx+='\n'+' '*(tab*2)+'<Path>%s</Path>'%(cgi.escape(str(form.getPath())))
			if form.method is not None:
				tmpx+='\n'+' '*(tab*2)+'<Method>%s</Method>'%(cgi.escape(str(form.method)))
			if form.getControls() is not None:
				for ctl in form.controls:
					tmpx+='\n'+' '*(tab*3)+'<Control>%s</Control>'%(cgi.escape(str(ctl)))
			tmpx+='\n'+' '*tab+'</Form>'
	########################## Fin Formularios ############
	########################## Recursos      #######################
	for pre,fill,node in RenderTree(bnode):
		if preant > len(pre): nums = 1 + (preant-len(pre)) / tab
		if preant == len(pre): nums=1
		while(nums>0):
			tmpx+='\n'+' '*(nums+1)*tab+"</Resource>"
			nums=nums-1
		tmpx+='\n'+' '*len(pre)+'<Resource>%s'%(cgi.escape(str(node.name)))
		if node.getStatus() is not None:
			tmpx+='\n'+' '*len(pre)+"<status>"+str(node.getStatus())+"</status>"
		for frm in node.getForms():
			#print frm
			# Chanfle pueden ser nulos
			if frm.name is not None:
				tmpx+='\n'+' '*len(pre)+cgi.escape(str(frm.name))+"<Formulario>"
			else:
				tmpx+='\n'+' '*len(pre)+"<Formulario>"
			if frm.action is not None:
				tmpx+='\n'+' '*(len(pre)+tab)+"<Action>%s</Action>"%(cgi.escape(str(frm.action)))
			if frm.name is not None:
				tmpx+='\n'+' '*len(pre)+cgi.escape(str(frm.name))+"</Formulario>"
			else:
				tmpx+='\n'+' '*len(pre)+"</Formulario>"
		preant=len(pre)
	nums=(preant)/tab+1
	#Agrego los ultimos /rec
	while(nums>0):
		#tmpx+='\n'+' '*(nums)*4+'</Resource>'
		tmpx+='\n'+' '*(nums)*tab+'</Resource>'
		nums = nums-1
	tmpx+="\n"
	return tmpx

#Busco el nodo que tenga esa ruta, lo regreso para despues modificar sus atributos
def buscaRuta(nodo,ruta):
	r = Resolver('name')
	actnode = None
	try:
		actnode = r.get(nodo,ruta)
		return actnode
	except Exception as ex:
		return None
		
def agrega(base,path):
	r = Resolver('name')
	try:
		if len(path)>0: # Busco si existe el nodo actual, si existe 
			actnode = r.get(base,path[0])
		if len(path) > 1: agrega(actnode,path[1:]) # Agrego los demas directorios , ie := actnode/../../
	except Exception:
		if len(path)>0:		# Si el nodo actual no existe lo agrego
			#nodo = Node(path[0],parent=base)
			nodo = simplenode(path[0],parent=base)
			# test
			'''
			print "parent path -> ",base.getFPath()
			print "nodo actual -> ",path[0]
			'''
			#print "parent -> ",base
			#print "tipo parent -> ",type(base)
			# Agrego la parte parcial de la url del padre
			nodo.setFPath(base.getFPath())
			# fin test
		# Agrego los demas nodos
		if len(path) > 1:
			agrega(nodo,path[1:])
'''
	bnde = string
'''
def buildMap(bnde,resources):
	'''
	print "ENtre a buildMap con ",bnde
	print bnde
	print "tipo ",type(bnde)
	'''
	bnode = simplenode(bnde,parent=None)
	bnode.setFPath()
	#print "<resources>\n",'\n'.join(resources),'\n</resources>'
	for res in resources:
		resource = res.split('//')[1]
		# Que pasa cuando no tiene el protocolo? tengo que ver si se realizo lo anterior
		dirlist = resource.split('/')[1:]
		agrega(bnode,dirlist)
	dom = ''.join(parseurls.getDomain(bnode.getUrl()).split('://')[1]).replace('www.','')
	try:
		RenderTreeGraph(bnode).to_picture(dom+'.jpg')
	except:
		print 'Cant write sitemap imagefile'
	return bnode

#clean resource url
def cleanrurl(rurl,rootnodeurl):
	# Tomamos despues del dominio
	newurl = rurl.replace(rootnodeurl,'')
	return newurl

'''
	Le paso los atributos
		dominio depth startpage bforce wlist cfgfile skipcerts 
'''
''' 
Debo dividir este metodo en dos.
	El primero regresa el sitemap en un nodo que debe recoger el crawler
		Buildsitemap debe 
	El segundo debe recibir ese nodo y una lista de recursos (objetos o no)
	mediante una bandera.
	Si starturl no tiene / al final se rompe 
'''
#def parseResources(rootnode,resources):
#def parseResources(fname,rootnode,resources,rootisleaf):
# chanfle: pasar los parametros de ejecucion para incluirlos en el xml
# ver si puedo pasar los formularios, si es posible, pasar como 
# parametro la lista de formularios y pasarlo directamente a sitexml
# 
def parseResources(fname,rootnode,resources,forms=None):
	rootisleaf=True
	if rootnode.endswith('/'):
		rootisleaf=False
	links  = []
	# Obtengo los links
	for r in resources: links.append(r.getUrl())
	# exp
	if rootisleaf: rootnode+='/'
	# Creacion de sitemap, se guarda en un nodo
	rnode = buildMap(rootnode,links)
	smap = sitemap(rnode)
	mpobj = mapobj(smap[0],smap[1])
	# Termine de crear el sitemap
	# Una vez que tengo el sitemap itero sobre los recursos para inyectar info
	for res in resources:
		resurl = res.getUrl()
		resurl = cleanrurl(resurl,rootnode)
		# Apartir del nodo raiz busco el nodo con la ruta resurl
		nactual = buscaRuta(rnode,resurl)
		# Pongo los atributos que tendra el nodo simple
		if nactual is not None:
			nactual.setForms(res.getForms())
			nactual.setStatus(res.getStatus())
	#########################################################
	# chanfle: aqui escribo el xml
	# regresarlo en el segundo elemento de la tupla
	sxml = siteXML(rnode,forms)
	mpobj.setXML(sxml)
	return mpobj
	
reload(sys)  
sys.setdefaultencoding('utf8')

from xml.dom.minidom import parse
class ConfigParser:
	def __init__(self,fname):
		# diccionario:= 'nombresw':pathescaner
		self.toolspath = {}
		# diccionario:= 'nombresw':[toolarg1,toolarg2...]
		self.toolargs = {}
		self.filename = fname
		self.toolflags = {}
		self.getToolsPath()
		self.getToolsArgs()
		self.getToolsFlags()
		
	# Regresa un diccionario  donde ('scannerdecms','path')
	# ie := 'wordpress','../wpscan'
	# Asi SWDetector puede preguntar en tiempo constante que herramientas tiene
	def getToolsPath(self):
		dom = parse(self.filename)
		# diccionario para las herramientas
		tools = {}
		xmltools=dom.getElementsByTagName('tool')
		for node in xmltools:
			tool_name=node.getAttribute('name')
			pathlist=node.getElementsByTagName('path')
			for p in pathlist: path = p.firstChild.data
			if path is not None:
				tools[tool_name] = path
		print('Debug: getToolsPath')
		print(tools)
		self.toolspath = tools
		
	# Construye un diccionario con entradas 'software':[arg1,arg2,...]
	def getToolsArgs(self):
		dom = parse(self.filename)
		# diccionario para las herramientas
		toolargs = {}
		args = []
		xmltools=dom.getElementsByTagName('tool')
		for node in xmltools:
			tool_name=node.getAttribute('name')
			pathlist=node.getElementsByTagName('targ')
			for p in pathlist: 
				args.append(p.firstChild.data)
			toolargs[tool_name] = args
			args = []
		self.toolargs = toolargs
		print('Debug: getToolsArgs')
		print(toolargs)
		return self.toolargs

	
	# regresa un diccionario donde la llave es el nombre de la herramienta
	# y el valor es una lista de tuplas donde la tupla es (marcador,score)
	def getToolsFlags(self):
		dom = parse(self.filename)
		toolflags = {}
		args = []
		xmltools=dom.getElementsByTagName('tool')
		for node in xmltools:
			tool_name=node.getAttribute('name')
			toolflags[tool_name] = []
			pathlist=node.getElementsByTagName('tflag')
			for p in pathlist: 
				tup = (str(p.firstChild.data),int(p.getAttribute('score')))
				toolflags[tool_name].append(tup)
		self.toolflags = toolflags
		print('Debug: getToolsFlags')
		print(toolflags)

	# Recibe el software (cms)  y regresa la cadena de comandos 
	# la herramienta debe sustituir su url
	def getToolArg(self,sw):
		if sw in self.toolspath:
			tpath = self.toolspath[sw]
			args = [tpath]
			args.extend(self.toolargs[sw])
			return args
		else:
			return None

	# Returns the scanner path for passed cms
	def getPath(self,cms):
		try:
			return self.toolspath[cms.lower()]
		except:
			return None		
	
	# regresa una lista de tuplas para las banderas de la herramienta externa
	#donde elem:=(marker,score)
	def getToolFlags(self,sw):
		if sw in self.toolflags:
			tflags = self.toolflags[sw]
			return tflags
		else:
			return None

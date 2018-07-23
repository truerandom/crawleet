class Formulario:
	def __init__(self,name,action,method,controls=[],path=''):
		self.path = path 
		self.name = name
		self.action = action
		self.method = method
		self.controls = controls
		
	def __str__(self):
		# return '\nName: '+self.name+"\nAction: "+self.action+"\nMethod: "+self.method+"\nControls:"+str(self.controls)+"\n"
		tmp = ''
		if self.name is not None and self.name !='': tmp+='\t'+self.name
		if self.action is not None: tmp+='\n\t'+self.action
		if self.method is not None: tmp+='\n\t'+self.method
		if self.getControls() is not None: tmp+='\n\t'+self.getControls()+'\n'
		return tmp
		#return '\tName: '+self.name+"\n\tAction: "+self.action+"\n\tMethod: "+self.method+"\n\tControls:"+self.getControls()+"\n"
		
	def addControl(self,control):
		self.controls.append(control)

	def setAction(self,action):
		if action is not None: self.action = action
	
	def setMethod(self,method):
		if method is not None:
			self.method = method
		
	def setControls(self,controles):
		self.controls = controles
		
	def setPath(self,path):
		self.path = path
	
	def getControls(self):
		ctls = ''
		for c in self.controls:
			ctls = ctls + '\n\t' + str(c)
		return ctls
	
	def getName(self):
		return self.name
		
	def getMethod(self):
		return self.method
		
	def getAction(self):
		return self.action
	# exp
	def getPath(self):
		return self.path
		
	# chanfle metodo nuevo
	def xml(self):
		tmp = '\n<formulario>\n<nombre>%s</nombre>\n<action>%s</action>\n<method>%s</method>' % (self.name,self.action,self.method)
		for c in self.controls:
			tmp+='\n<control>%s</control>'%(c)
		tmp+='\n</formulario>'
		return tmp

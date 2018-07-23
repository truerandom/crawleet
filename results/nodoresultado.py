from anytree import *
#chanfle muy sucio :V
class resultado(object): test = 1

class nodoresultado(resultado,NodeMixin):
	def __init__(self,url,purl,nivel,parent=None):
		super(resultado,self).__init__()
		self.url = url
		self.purl = purl
		self.nivel = nivel
		self.status = None
		self.forms = []
		self.links = []
		self.parent = parent

	def setUrl(self,url): self.url = url
	def setPUrl(self,purl): self.purl = purl
	def setStatus(self,status): self.status = status
	def setForms(self,forms): self.forms = forms
	def setLinks(self,links): self.links = links
	def getUrl(self): return self.url
	def getPUrl(self): return self.purl
	def getNivel(self): return self.nivel
	def getStatus(self): return self.status
	def getParent(self): return self.parent
	def getLinks(self): return self.links
	def getForms(self): return self.forms
	def hasForms(self):
		if len(self.forms) == 0: 
			return False
		return True
	def __str__(self):
		return "Url: "+self.url+" Nivel "+str(self.nivel)+" Purl "+self.purl+" Status: "+str(self.status)+" #forms "+str(len(self.getForms()))+" #links "+str(len(self.links))

	def xml(self):
		tmp = ''
		tmp+='<resultado>\n<url>%s</url>\n<nivel>%s</nivel>\n<status>%s</status>' % (self.url,self.nivel,self.status)
		for s in self.forms:
			#Aqui falta el metodo xml
			tmp+='\n'+s.xml()
		tmp+='\n</resultado>'
		return tmp

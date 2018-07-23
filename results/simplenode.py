from anytree import *
#chanfle muy sucio :V
class simplen(object): test = 1
class simplenode(simplen,NodeMixin):
	def __init__(self,url,parent=None):
		super(simplen,self).__init__()
		self.url = url
		self.name = url
		self.parent = parent
		self.status = None
		self.dirlisting = None
		self.forms = []
		self.fpath = None
		
	def setUrl(self,url):
		self.url = url
		
	def setStatus(self,status):
		self.status = status
		
	def setForms(self,forms):
		self.forms = forms
	def setDirListing(self,dirlisting): self.dirlisting = dirlisting
	def getUrl(self): return self.url
	def getStatus(self): return self.status
	def getForms(self): return self.forms
	# chanfle
	def setFPath(self,parentpath=None):
		'''
		print "#"*30
		print "entre a setparentpath snode con parentpath ",parentpath
		'''
		try:
			if parentpath is not None:
				self.fpath = parentpath+'/'+self.url
			else:
				self.fpath = self.url
		except:
			self.fpath = self.url
		
	def getFPath(self):
		return self.fpath
		
	def hasForms(self):
		if len(self.forms) == 0: return False
		return True
		
	def __str__(self):
		try:
			return "Url: "+self.url+" Status: "+str(self.status)+"parent"+self.parent+" #forms "+str(len(self.getForms()))
		except:
			return "Url: "+self.url+" Status: "+str(self.status)+" #forms "+str(len(self.getForms()))

	def xml(self):
		#tmp='<resultado>\n<url>%s</url>\n<status>%s</status>' % (self.url,self.status)
		tmp='<resultado>\n<url>%s</url>' % (self.url,self.status)
		for s in self.forms:
			tmp+=s.xml()
		tmp+='\n</resultado>'
		return tmp

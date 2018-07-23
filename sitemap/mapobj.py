class mapobj:
	def __init__(self,smap=None,absurls=None,xml=None):
		self.smap=smap
		self.absurls = absurls
		self.xml = xml
		
	def setMap(self,smap=None):
		self.smap = smap

	def setAbsUrls(self,absurls=None):
		self.absurls = absurls

	def setXML(self,xml=None):
		self.xml = xml
		
	def getMap(self):
		return self.smap
		
	def getAbsUrls(self):
		return self.absurls

	def getXML(self):
		return self.xml
	
	def __str__(self):
		return "MapObj"


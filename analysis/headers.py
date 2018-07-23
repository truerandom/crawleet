# Returns if options is enabled
def getHeaders(req,host):
	try:
		return req.getHTMLCode(host).headers
	except Exception as e:
		return None

# Returns headers with sensitive info
def getInfoHeaders(req,host):
	try:
		hs = ['Server', 'Via', 'X-Powered-By', 'X-Country-Code','E-Tag'
		'Authorization','WWW-Authenticate','Proxy-Authenticate','Proxy-Authorization',
		'Accept','X-JAL','X-JSL','Cookie','X-AspNet-Version','X-Accel-Version',
		'X-Whom','X-Cache','X-Generator','X-Forwarded-For','X-Forwarded-By',
		'X-Drupal-Cache','CF-RAY','X-Varnish']
		foundheaders = getHeaders(req,host)
		headers = ['************ Info Headers **************']
		if foundheaders is not None:
			for header in hs:
				# if header in busca
				if header in foundheaders.keys():
					#print 'header %s value %s ' % (header,foundheaders[header])
					headers.append('%s: %s' % (header,foundheaders[header]))
		return headers
	except Exception as e:
		return None

'''
Busca una serie de headers definidos en una lista y regresa una lista
con el valor para los que estan y reporta si no estan
'''
def secureHeaders(req,host):
	try:
		hs = ['X-Content-Type-Options','X-Frame-Options',
		'Strict-Transport-Security',
		'X-XSS-Protection','Content-Security-Policy','Public-Key-Pins']
		foundheaders = getHeaders(req,host)
		headers = ['************Secure Headers**************']
		notfoundheaders=['*********Missing Secure Headers*********']
		if foundheaders is not None:
			for header in hs:
				if header in foundheaders.keys():
					headers.append('%s: %s' % (header,foundheaders[header]))
				else:
					notfoundheaders.append('%s not found'%header)
		res = []
		if len(headers)>1: res = res+headers
		if len(notfoundheaders) > 1: res = res+notfoundheaders
		return res
	except Exception as e:
		return None


def headersAnalysis(req,host):
	return getInfoHeaders(req,host)+secureHeaders(req,host)


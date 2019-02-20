# Returns if options is enabled
def getHeaders(req,host):
	try:
		return req.getHTMLCode(host).headers
	except Exception as e:
		return None

# Returns headers with sensitive info
def getInfoHeaders(req,host):
	try:
		hs = ['last-modified','server', 'via', 'x-powered-by', 'x-country-code','e-tag'
		'authorization','www-authenticate','proxy-authenticate','proxy-authorization',
		'accept','x-jal','x-jsl','cookie','x-aspnet-version','x-accel-version',
		'x-whom','x-cache','x-generator','x-forwarded-for','x-forwarded-by',
		'x-drupal-cache','cf-ray','x-varnish']
		foundheadersorig = getHeaders(req,host)
		foundheaders = {}
		for key, value in foundheadersorig.iteritems():
			foundheaders[key.lower()] = value
		headers = ['************ Info Headers **************']
		if foundheaders is not None:
			for header in hs:
				# if header in busca
				if header in foundheaders.keys():
					#print 'header %s value %s ' % (header,foundheaders[header])
					headers.append('%s: %s' % (header,foundheaders[header]))
		return headers
	except Exception as e:
		return []

'''
Busca una serie de headers definidos en una lista y regresa una lista
con el valor para los que estan y reporta si no estan
'''
def secureHeaders(req,host):
	try:
		hs = ['x-content-type-options','x-frame-options',
		'strict-transport-security',
		'x-xxs-protection','content-security-policy','public-key-pins']
		foundheadersorig = getHeaders(req,host)
		foundheaders = {}
		for key, value in foundheadersorig.iteritems():
			foundheaders[key.lower()] = value
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
		return []


def headersAnalysis(req,host):
	return getInfoHeaders(req,host)+secureHeaders(req,host)


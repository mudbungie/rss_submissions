import urllib.parse
import dsportal
import cgitb
import cgi
import rssgen

cgitb.enable()

def application(env, start_response):
	method = env['REQUEST_METHOD']
	try:
		contentLength = int(env['CONTENT_LENGTH'])
		postEnv = env.copy()
		postEnv['QUERY STRING'] = ''
		HTTPPost = cgi.FieldStorage(fp = env['wsgi.input'], environ = postEnv, keep_blank_values = True)
	except ValueError:
		pass
	

	path = env['PATH_INFO']

	if path == '/post':
		start_response('200 OK', [('Content-Type', 'text/html; charset = utf-8')])
		return(dsportal.post())
	elif path == '/form':
		start_response('200 OK', [('Content-Type', 'text/html; charset = utf-8')])
		return(dsportal.form())
	elif method == 'POST':
		start_response('200 OK', [('Content-Type', 'application/xml; charset = utf-8')])
		return(dsportal.preview(HTTPPost))
	else:
		start_response('200 OK', [('Content-Type', 'application/xml; charset = utf-8')])
		return(rssgen.feed())	

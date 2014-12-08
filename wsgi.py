import urllib.parse
import dsportal

def application(env, start_response):
	method = env['REQUEST_METHOD']
	try:
		contentLength = int(env['CONTENT_LENGTH'])
		post = (env['wsgi.input'].read(contentLength).decode())
	except:
		ValueError
		raise
	
	start_response('200 OK', [('Content-Type', 'text/html; charset = utf-8')])
	
	if method == 'POST':
		for item in post.split('Content-Disposition: form-data'):
			yield(item.encode('utf-8') + '^^^'.encode('utf-8'))
#		return(post.encode('utf-8'))
#		return(dsportal.post(post))
	else:
		return(dsportal.form())	

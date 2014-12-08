def form():
	return '''
<!DOCTYPE html>
<head>
	<title>DeskSite RSS Feed Submission</title>
</head>

<body>
	<form 	name = "DeskSite RSS Submission"
		action = "wsgi.py"
		method = "POST"
		enctype = "multipart/form-data"
	>
	<b>Don't be stupid</b>
	<br>
	<p>Title:</p><input type="text" size="25" name="title"><p>The title of the video. Max 60 characters.</p><hr>
	<p>Description:</p><input type="text" size="50" name="description"><p>Description for the video</p><hr>
	<p>Keywords:</p><input type="text" size="25" name="keywords"><p>Contextual keywords per content item. Multiple keywords can be specified in a single node separated by commas. Max three keywords.</p><hr>
	<p>Caption:</p><input type="text" size="25" name="caption"><p>Caption to display under the video</p><hr>
<!--	<p>Video File:</p><input type="file" name="uploadVideo"><hr>
	<p>Thumbnail File:</p><input type="file" name="uploadThumbnail"><hr>
--!>
	<input type="submit" value="Demo Video">
<!--	<input type="submit" value="Submit Video">
--!>
	<br>
	</form>
	<br>
	<a href=deletion.html>I have told Megan that I posted a video in error, and deleting it is only one of the many steps being taken to remediate my degeneracy and incompetence.</a>
</body>
'''.encode('utf-8')

'''
def post(httpPost):
	response = []

	# generic function to test the strings given against our limiting parameters
	def verifyPostField(	field, fieldSoftName, maxlength, minlength, 
				restrictedChar = False, restrictedCharMin = 0, restrictedCharMax = 0):
		if len(field) > maxlength:
			return False, fieldSoftName + ' is too long.'
		elif len(field) > minlength:
			return False, fieldSoftName + ' is too short.'
		if restrictedChar:
			if field.count(restrictedChar) <= restrictedCharMin:
				return False, fieldSoftName + ' has too many delimiters.'
			if field.count(restrictedChar) >= restrictedCharMax:
				return False, fieldSoftName + ' has too few delimiters.'
		else:
			return True, fieldSoftName + ' passes basic muster.'

	titleVerification = verifyPostField(httpPost['title'], 60, 1)
	response.append(titleVerification[1])
	descriptionVerification = verifyPostField(httpPost['description'], 350, 1)
	response.append(descriptionVerification[1])
	keywordsVerfication = verifyPostField(httpPost['keywords'], 150, 6, ',', 3, 3)
	response.append(keywordsVerification[1])
	captionVerification = verifyPostField(httpPost['caption'], 60, 1)
	response.append(captionVerification[1])

	if 	titleVerification[0] == True and
		descriptionVerification[0] == True and
		keywordsVerification[0] == True and
		captionVerification[0] == True:
'''

def post(httpPost):
	for i in httpPost:
		yield(i.encode('utf-8'))

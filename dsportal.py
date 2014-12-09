import xmlgen
import uuid
import datetime

def form():
	with open('dsportal.html', 'r')	as html:
		yield(html.read().encode('utf-8'))

def writeItem(title, guid, description, keywords):
	# initialize the tags
	item = xmlgen.XMLEnclosedTag('item')
	itemGuid = xmlgen.XMLEnclosedTag('guid')
	itemGuid.addContent(guid)
	itemTitle = xmlgen.XMLEnclosedTag('title')
	itemTitle.addContent(title)
	itemDescription = xmlgen.XMLEnclosedTag('description')
	itemDescription.addContent(description)
	itemAuthor = xmlgen.XMLEnclosedTag('author')
	itemAuthor.addContent('DeskSite')
	itemMediaContent = xmlgen.XMLEnclosedTag('media:content')
	itemMediaContent.addAttrib('duration', 'GOTTA DERIVE THIS')
	itemMediaContent.addAttrib('type', 'video/mp4')
	itemMediaContent.addAttrib('url', 'GOTTA DERIVE THIS')
	itemMediaThumbnail = xmlgen.XMLTag('media:thumbnail')
	itemMediaThumbnail.addAttrib('url', 'GOTTA DERIVE THIS')
	itemMediaThumbnail.addAttrib('type', 'image/jpeg')
	itemMediaThumbnail.addAttrib('height', 'GOTTA DERIVE THIS')
	itemMediaThumbnail.addAttrib('width', 'GOTTA DERIVE THIS')
	itemMediaTitle = xmlgen.XMLTag('media:title')
	itemMediaTitle.addContent(title)
	itemMediaCopyright = xmlgen.XMLEnclosedTag('media:copyright')
	itemMediaCopyright.addContent('DeskSite')
	itemPubDate = xmlgen.XMLEnclosedTag('pubdate')
	itemPubDate.addContent(datetime.datetime.now().isoformat().split('.')[0])
	itemMediaKeywords = xmlgen.XMLEnclosedTag('media:keywords')
	itemMediaKeywords.addContent(keywords)

	item.addChildTag(itemGuid)
	item.addChildTag(itemTitle)
	item.addChildTag(itemDescription)
	item.addChildTag(itemAuthor)
	item.addChildTag(itemMediaContent)
	item.addChildTag(itemPubDate)
	item.addChildTag(itemMediaKeywords)

	itemMediaContent.addChildTag(itemMediaThumbnail)
	itemMediaContent.addChildTag(itemMediaTitle)
	itemMediaContent.addChildTag(itemMediaText)
	itemMediaContent.addChildTag(itemMediaCopyright)
	
	return item.publish()

def parseInput(httpPost):
	httpPostSplit = httpPost.split('WebKitFormBoundary')
	boundaryString = httpPostSplit[0]
	for grouping in httpPost.split(WebKitFormBoundary):
		

def post(httpPost):
	# takes a dict of values from the form
	response = []

	# generic function to test the strings given against our limiting parameters
	def verifyPostField(	field, fieldSoftName, maxlength, minlength, 
				restrictedChar = False, restrictedCharMin = 0, restrictedCharMax = 0):
		if len(field) > maxlength:
			return False, fieldSoftName + ' is too long.'
		elif len(field) < minlength:
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

	if( titleVerification[0] == True and
		descriptionVerification[0] == True and
		keywordsVerification[0] == True):
		
		guid = uuid.uuid4()
		item = writeItem(title, guid, description, keywords)
		return item.emcode('utf-8')
			

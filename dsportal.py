import xmlgen
import uuid
import datetime
import cgi
import subprocess
import os
import rssgen

PathToContent = 'content/'

class UserError(Exception):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return message

class thumbnail:
	def __init__(self, imageFile):
		metadataExtractionCommand = 'identify ' + PathToContent + imageFile + ' -verbose'
		self.fileName = imageFile
		metadata = subprocess.check_output(metadataExtractionCommand, shell=True).decode('UTF=8').split(' ')
		self.type = metadata[1]
		self.resolution = metadata[2]
		self.width = self.resolution.split('x')[0]
		self.height = self.resolution.split('x')[1]

class video:
	def getDuration(self, durationLine):
		durationInSeconds = 0
		listIndex = 0
		durationLineSplit = durationLine.split(' ')
		for timeQuantity in durationLineSplit:
			listIndex = listIndex + 1
			if timeQuantity.endswith('h'):
				durationInSeconds = durationInSeconds + (int(timeQuantity.split('h')[0]) * 3600)
			if timeQuantity.endswith('mn'):
				durationInSeconds = durationInSeconds + (int(timeQuantity.split('mn')[0]) * 60)
			if timeQuantity.endswith('s') and not timeQuantity.endswith('ms'):
				durationInSeconds = durationInSeconds + (int(timeQuantity.split('s')[0]))
		return str(durationInSeconds)
	def __init__(self, videoFile):
		self.fileName = videoFile
		metadataExtractionCommand = 'mediainfo ' + PathToContent + self.fileName
		# takes all the metadata and gives a list of strings
		metadata = subprocess.check_output(metadataExtractionCommand, shell=True).decode('UTF=8').split('\n')
		for line in metadata:
			if line.startswith('Duration'):
				self.duration = self.getDuration(line.split(':')[1])
		self.type = ('video/mp4')

def form():
	with open('dsportal.html', 'r')	as html:
		yield(html.read().encode('utf-8'))

def writeItem(postStrings):
	feedURL = 'http://desksitedemo.cloudapp.net/'
	contentURIFragment = 'content/'
	contentURL = feedURL + contentURIFragment
	
	# I'm honestly just extracting these because it makes it easier to read in the XML knot.
	title = postStrings['title']
	guid = postStrings['guid']
	description = postStrings['description']
	keywords = postStrings['keywords']
	pubDate = postStrings['pubDate']
	postThumbnail = postStrings['uploadThumbnail']
	postVideo = postStrings['uploadVideo']
	postThumbnailHeight = postStrings['uploadThumbnailHeight']
	postThumbnailWidth = postStrings['uploadThumbnailWidth']
	postVideoDuration = postStrings['uploadVideoDuration']

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
	itemMediaContent.addAttrib('duration', postVideoDuration)
	itemMediaContent.addAttrib('type', 'video/mp4')
	itemMediaContent.addAttrib('url', contentURL + postVideo)
	itemMediaThumbnail = xmlgen.XMLTag('media:thumbnail')
	itemMediaThumbnail.addAttrib('url', contentURL + postThumbnail)
	itemMediaThumbnail.addAttrib('type', 'image/jpeg')
	itemMediaThumbnail.addAttrib('height', postThumbnailHeight)
	itemMediaThumbnail.addAttrib('width', postThumbnailWidth)
	itemMediaTitle = xmlgen.XMLEnclosedTag('media:title')
	itemMediaTitle.addContent(title)
	itemMediaCopyright = xmlgen.XMLEnclosedTag('media:copyright')
	itemMediaCopyright.addContent('DeskSite')
	itemPubDate = xmlgen.XMLEnclosedTag('pubdate')
	itemPubDate.addContent(pubDate)
	itemMediaKeywords = xmlgen.XMLEnclosedTag('media:keywords')
	itemMediaKeywords.addContent(keywords)
	print(itemMediaThumbnail.values['url'])

	# wrap up the XML
	item.addChildTag(itemGuid)
	item.addChildTag(itemTitle)
	item.addChildTag(itemDescription)
	item.addChildTag(itemAuthor)
	item.addChildTag(itemMediaContent)
	item.addChildTag(itemPubDate)
	item.addChildTag(itemMediaKeywords)

	itemMediaContent.addChildTag(itemMediaThumbnail)
	itemMediaContent.addChildTag(itemMediaTitle)
	itemMediaContent.addChildTag(itemMediaCopyright)

	completedItem = item.publish()
	# return it as a big string
	with open('preview/' + pubDate + postVideo + '.xml', 'w') as xmlFile:
		xmlFile.write(completedItem)
	return completedItem
	
def parseHTTPPost(HTTPPost):
	# takes the FieldStorage object, does verification, and returns a dict of strings
	# for the simple values, these are unmodified from the original contents of HTTPPost,
	# with the exception of character substution for dangerous or unsupported characters
	# For files, this saves them to the CDN directory under unique names, and returns 
	# those file names. I'm also generating the uuid/pubdate in here. That is partly because
	# I might want to make uuids/pubdates submittable in the future, and partly because it
	# just feels neater to do everything in here.
	postParsed = {}
	postParsed['pubDate'] = datetime.datetime.now().isoformat().split('.')[0]
	postParsed['guid'] = str(uuid.uuid4().int)

	# do all the things necessary to make sure that we aren't proceeding with strings
	# that we can safely use
	def verifyString(HTTPPost, fieldName):
		field = HTTPPost[fieldName].value

		# cut out those stupid quotes that Word uses

		# cut out characters poisonous to XML
		field = field.replace('&', '&amp;')
		field = field.replace('\"', '&quot;')
		field = field.replace('\'', '&apos;')
		field = field.replace('<', '&lt;')
		field = field.replace('>', '&gt;')
		
		# assign limitations specific to the different strings
		if fieldName == 'title':
			maxLength = 60
			minLength = 1
		elif fieldName == 'description':
			maxLength = 350
			minLength = 1
		elif fieldName == 'keywords':
			maxLength = 250
			minLength = 5
			delimitingChar = ','
			numberOfDelimiters = 2
		else:
			raise UserError(fieldName)
		# check those limitations
		if len(field) > maxLength:
			raise UserError(fieldName + ' too long')
		elif len(field) < minLength:
			raise UserError(fieldName + ' too short')
		try:
			if field.count(delimitingChar) != numberOfDelimiters:
				raise UserError(fieldName + ' has the wrong number of delimiters')
		except NameError:
			# because only keywords actually have this field
			pass
		return field

	postParsed['title'] = verifyString(HTTPPost, 'title')
	postParsed['description'] = verifyString(HTTPPost, 'description')
	postParsed['keywords'] = verifyString(HTTPPost, 'keywords')

	# takes a file and its name, saves it, returns the filename
	def saveUpload(upload, postDict):
		uploadFileName = postDict['pubDate'].replace(':', '_') + upload.filename
		with open(PathToContent + uploadFileName, 'wb') as uploadFile:
			uploadFile.write(upload.value)
		return uploadFileName

	postParsed['uploadThumbnail'] = saveUpload(HTTPPost['uploadThumbnail'], postParsed)
	postThumbnail = thumbnail(postParsed['uploadThumbnail'])
	postParsed['uploadThumbnailHeight'] = postThumbnail.height
	postParsed['uploadThumbnailWidth'] = postThumbnail.width

	postParsed['uploadVideo'] = saveUpload(HTTPPost['uploadVideo'], postParsed)
	postVideo = video(postParsed['uploadVideo'])
	postParsed['uploadVideoDuration'] = postVideo.duration

	return postParsed

def preview(HTTPPost):
	# clear out any old previews
	for listing in os.listdir(path = 'preview/'):
		os.remove('preview/' + listing)
	
	# turn the post into a bunch of strings
	postStrings = parseHTTPPost(HTTPPost)

	# write it out in XML
	postXML = writeItem(postStrings)

	# wrap it up with a preview RSS page so that browsers know how to render it
	demoRSS = rssgen.demo(postXML)
	
	# give it to the browser
	return demoRSS

def post():
	for listing in os.listdir(path = 'preview/'):
		os.rename('preview/' + listing, 'items/' + listing)
	return ('Post made live')

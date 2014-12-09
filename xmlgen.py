# XML generator

class XMLTag:
	def __init__(self, tag):
		self.tag = tag
	def addAttrib(attrib, value=None):
		attribs.append(attrib)
		if value:
			values.append(attrib, value)
	def publish():
		tagString = '<' + self.tag
		for attrib in attribs:
			tagString = tagString + ' ' + attrib
			if value in valus[attrib]:
				tagstring = tagString + '=' + '"' + value + '"'
		tagString = tagString + '>'
		return tagString

class XMLEnclosedTag(XMLTag):
	def __init__(self, tag):
		self.tag = tag
		self.childTags = []
		self.attribs = []
		self.values = {}
		self.content = ''
	def addChildTag(child):
		self.childTags.append(child)
	def addContent(content):
		self.content = self.content + content
	def publish():
		tagString = '<' + self.tag
		for attrib in self.attribs:
			tagString = tagString + ' ' + attrib
			if value in self.values[attrib]:
				tagstring = tagString + '=' + '"' + value + '"'
		tagString = tagString + '>'
		for child in self.childTags:
			self.content = self.content + child.publish()
		tagString = tagString + self.content
		tagString = tagString + '</' + self.tag + '>'
		return tagString


#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import addonHandler
addonHandler.initTranslation()

import lxml.html

name = u'Dictionary box'
url_request = u'http://dictionarybox.com/result.asp?pl-dbox-search-field={text}&pl-dbox-langs=EnglishToRussian,RussianToEnglish'

def sendRequest(text):
	text = text.strip(u' \n\t!@#$%^&*()_+=-"№;:?<>{}[]~`')
	response = lxml.html.parse(url_request.format(text=text)).getroot()
	return response.xpath('//div')

def parseResponse(response):
	if not response:
		return _('No results')
	result = []
	for i in response[1:]:
		result.append(i.text_content())
	return '<br>'.join(result).encode('raw-unicode-escape').decode('utf-8').replace('\n', '<br>')

def getResult(text, lang=None, calback=None):
	# argument "lang" is not using here
	calback(parseResponse(sendRequest(text)), name, True)
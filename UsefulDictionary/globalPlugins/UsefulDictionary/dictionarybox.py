#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import lxml.html

name = u'Dictionary box'
url_request = u'http://dictionarybox.com/result.asp?pl-dbox-search-field={text}&pl-dbox-langs=EnglishToRussian,RussianToEnglish'

def sendRequest(text):
	response = lxml.html.parse(url_request.format(text=text)).getroot()
	return response.xpath('//div')

def parseResponse(response):
	if not response:
		return u'No results'
	result = []
	for i in response[1:]:
		result.append(i.text_content())
	return '\n'.join(result).encode('raw-unicode-escape').decode('utf-8').replace(';', '.')

def getResult(text):
	return parseResponse(sendRequest(text))
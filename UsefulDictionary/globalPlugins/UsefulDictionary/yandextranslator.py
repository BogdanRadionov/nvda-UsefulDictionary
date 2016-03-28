#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import urllib2
import json

name = _(u'Yandex translator')
url_request = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20160311T160508Z.34101ab79242d6fd.120d4f5b06e2efd6dfbd194e5aa9756df01bfcda&text={text}&lang={lang}'

def sendRequest(text, lang):
	text = text.encode('utf-8')
	return json.load(urllib2.urlopen(url_request.format(text=text, lang=lang)))

def parseResponse(response):
	return '\n'.join(response['text']).replace(';', '.')

def getResult(text, lang, calback):
	result = parseResponse(sendRequest(text, lang))
	calback(result, name)
#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import addonHandler
addonHandler.initTranslation()

import urllib2
import json
import proxy
import _config
import requests

name = _(u'Yandex translator')
url_request = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20160311T160508Z.34101ab79242d6fd.120d4f5b06e2efd6dfbd194e5aa9756df01bfcda&text={text}&lang={lang}'

def sendRequest(text, lang):
	text = urllib2.quote(text.encode('utf-8'))
	if _config._conf['proxy']:
		if _config._conf['proxy_address'] is None:
			p = proxy.Proxies()
			proxy_addr = p.next_proxy()
			_config._conf['proxy_address'] = proxy_addr
			_config.save_config()
		else:
			proxy_addr = _config._conf['proxy_address']
		return json.loads(requests.get(url_request.format(text=text, lang=lang), proxies={'https': proxy_addr}).text)
	return json.loads(requests.get(url_request.format(text=text, lang=lang)).text)

def parseResponse(response):
	return '\n'.join(response['text'])

def getResult(text, lang, calback):
	result = parseResponse(sendRequest(text, lang))
	calback(result, name)
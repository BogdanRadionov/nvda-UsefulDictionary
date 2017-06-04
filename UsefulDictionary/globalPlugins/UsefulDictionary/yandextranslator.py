#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import addonHandler
addonHandler.initTranslation()

import urllib2
import json
import proxy
import _config
import requests
import ui

name = _(u'Yandex translator')
url_request = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20160311T160508Z.34101ab79242d6fd.120d4f5b06e2efd6dfbd194e5aa9756df01bfcda&text={text}&lang={lang}'

def sendRequest(text, lang):
	conf = _config.load_config()
	text = urllib2.quote(text.encode('utf-8'))
	if conf['proxy']:
		if conf['proxy_address'] is None:
			ui.message(_('Searching proxy server'))
			p = proxy.Proxies()
			proxy_addr = p.next_proxy()
			conf['proxy_address'] = proxy_addr
			_config.save_config(conf)
		else:
			proxy_addr = conf['proxy_address']
		return json.loads(requests.get(url_request.format(text=text, lang=lang), proxies={'https': proxy_addr}).text)
	return json.loads(requests.get(url_request.format(text=text, lang=lang)).text)

def parseResponse(response):
	return '\n'.join(response['text'])

def getResult(text, lang, calback):
	result = parseResponse(sendRequest(text, lang))
	calback(result, name)
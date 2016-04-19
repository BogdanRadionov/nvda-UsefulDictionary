#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>
import addonHandler
addonHandler.initTranslation()

import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
name = u'Mediawiki'

def parseResponse(response):
	result = []
	result.append('<h1>'+response.original_title+'</h1>')
	content = response.content.replace('\n', '<br>').replace('<br>== ', '<h2>').replace(' ==<br>', '</h2>').replace('<br>=== ', '<h3>').replace(' ===<br>', '</h3>').replace('<br>==== ', '<h4>').replace(' ====<br>', '</h4>')
	result.append(content)
	result.append('<br><h6>'+_('Similar results:')+'</h6>')
	result.append('<br>'.join(wikipedia.search(response.title)).replace(';', '.'))
	result.append(u'<a href="{0}">{1}</a>'.format(response.url, _('Link on page')))
	return ''.join(result)

def getResult(text, lang, calback=None):
	wikipedia.set_lang(lang)
	try:
		result = parseResponse(wikipedia.page(text))
	except (PageError, DisambiguationError):
		result = []
		result.append('<h1>' + _('No results') + '</h1>')
		similar = '<br>'.join(wikipedia.search(text))
		if similar:
			result.append('<br><h6>'+_('Similar articles:')+'</h6>')
			result.append(similar)
		result = ''.join(result)
	calback(result, name, True)
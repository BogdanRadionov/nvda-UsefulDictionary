#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
name = u'Mediawiki'

# pattern_header = re.compile(r'^== .*? ==$', re.MULTILINE)

def parseResponse(response):
	result = []
	result.append('<h1>'+response.original_title+'</h1>')
	content = response.content.replace(';', '.').replace('\n', '<br>').replace('<br>== ', '<h2>').replace(' ==<br>', '</h2>').replace('<br>=== ', '<h3>').replace(' ===<br>', '</h3>').replace('<br>==== ', '<h4>').replace(' ====<br>', '</h4>')
	result.append(content)
	result.append('<br><h6>'+'Similar results:'+'</h6>')
	result.append('<br>'.join(wikipedia.search(response.title)).replace(';', '.'))
	result.append('<a href="{0}">{1}</a>'.format(response.url, 'Link on page'))
	return ''.join(result)

def getResult(text, lang, calback=None):
	wikipedia.set_lang(lang)
	try:
		result = parseResponse(wikipedia.page(text))
	except (PageError, DisambiguationError):
		result = 'No results'
	calback(_(result), name, True)
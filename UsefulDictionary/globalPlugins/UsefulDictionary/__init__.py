#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import os
import sys
import addonHandler

basepath = os.path.dirname(__file__)
sys.path.append(basepath)
sys.path.append(os.path.join(basepath, 'lib'))
addonHandler.initTranslation()

from globalPluginHandler import GlobalPlugin
import api
import ui
import textInfos
import threading
import _config

_config.load_config()
_conf = _config._conf
_dict = __import__(_conf['selected_dict'])

dictionaries = {
	'dictionarybox': ['auto'],
	'mediawiki': ['ru', 'en'],
	'yandextranslator': ['en-ru', 'ru-en'],
}

def getSelectedText():
	focus = api.getFocusObject()
	treeInterceptor = focus.treeInterceptor
	if hasattr(treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
		focus = treeInterceptor
	try:
		info = focus.makeTextInfo(textInfos.POSITION_SELECTION)
	except (RuntimeError, NotImplementedError):
		info=None
	if not info or info.isCollapsed:
		return ui.message(_('No selected text'))
	else:
		return info.text

class GlobalPlugin(GlobalPlugin):
	def script_openDictionary(self, gesture):
		text = getSelectedText()
		if text:
			ui.message(_('Looking for information'))
			t = threading.Thread(target=_dict.getResult, args=[text, _conf[_conf["selected_dict"]], ui.browseableMessage])
			t.start()

	def script_swithLang(self, gesture):
		num_lang = dictionaries[_conf['selected_dict']].index(_conf[_conf['selected_dict']]) 
		if num_lang >= len(dictionaries[_conf['selected_dict']])-1:
			_conf[_conf['selected_dict']] = dictionaries[_conf['selected_dict']][0]
		else:
			_conf[_conf['selected_dict']] = dictionaries[_conf['selected_dict']][num_lang+1]
		ui.message(_('Selected language: {0}').format(_conf[_conf['selected_dict']]))
		_config.save_config()

	def script_swithDict(self, gesture):
		global _dict
		dicts = sorted(dictionaries.keys())
		num_selected_dict = dicts.index(_conf['selected_dict'])
		if num_selected_dict >= len(dicts)-1:
			_dict = __import__(dicts[0])
			_conf['selected_dict'] = dicts[0]
		else:
			_dict = __import__(dicts[num_selected_dict+1])
			_conf['selected_dict'] = dicts[num_selected_dict+1]
		_config.save_config()
		ui.message(_('Dictionary selected: {0}').format(_dict.name))
		ui.message(_('Language: {0}').format(_conf[_conf['selected_dict']]))

	def script_binding(self, gesture):
		ui.message(_('This hotkey is bound to the UsefulDictionary addon but is not currently being used'))

	script_openDictionary.__doc__=_('Send selected text to chosen resourse')

	__gestures = {
		"kb:nvda+w": "openDictionary",
		"kb:nvda+shift+w": "binding",
		"kb:nvda+control+w": "swithLang",
		"kb:nvda+control+shift+w": "swithDict",
	}
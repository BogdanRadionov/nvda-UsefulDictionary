#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import os
import sys

basepath = os.path.dirname(__file__)
sys.path.append(os.path.join(basepath, 'lib'))

from globalPluginHandler import GlobalPlugin
import api
import ui
import textInfos
import addonHandler
import dictionarybox

addonHandler.initTranslation()

dictionaries = [
	'dictionarybox',
]

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
			ui.browseableMessage(dictionarybox.getResult(text), dictionarybox.name)

	def script_binding(self, gesture):
		ui.message(_('This hotkey is bound to the UsefulDictionary addon but is not currently being used'))

	__gestures = {
		"kb:nvda+shift+w": "openDictionary",
		"kb:nvda+control+w": "binding",
		"kb:nvda+control+shift+w": "binding",
	}
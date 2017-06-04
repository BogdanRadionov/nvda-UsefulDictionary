# -*- coding:utf-8 -*-

# Copyright Bogdan Radionov <radionov.bogdan@gmail.com>

import gui
import wx
import _config

class SettingsDialog(gui.SettingsDialog):
	title = _('Usefull Dictionary Settings')
	def __init__(self, parent):
		super(SettingsDialog, self).__init__(parent)

	def makeSettings(self, sizer):
		conf = _config.load_config()
		self.proxyCHK = wx.CheckBox(self, label=_('Use proxy'))
		self.proxyCHK.SetValue(conf['proxy'])
		sizer.Add(self.proxyCHK)

	def onOk(self, evt):
		super(SettingsDialog, self).onOk(evt)
		conf = _config.load_config()
		conf['proxy'] = self.proxyCHK.GetValue()
		conf['proxy_address'] = None
		_config.save_config(conf)

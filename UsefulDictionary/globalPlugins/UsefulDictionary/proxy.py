# -*- coding:utf-8 -*-

# Copyright Bogdan Radionov <radionov.bogdan@gmail.com>

import lxml.html

resource_proxies = 'http://www.sslproxies.org/'

class Proxies(object):
	def __init__(self):
		self.proxies = []
		self.response = lxml.html.parse(resource_proxies).getroot()
		for p in self.response.xpath("id('proxylisttable')/tbody/tr"):
			if p.xpath('td[5]')[0].text_content() == 'anonymous' and p.xpath('td[7]')[0].text_content() == 'yes' and p.xpath('td[3]')[0].text_content() != 'UA' and p.xpath('td[4]')[0].text_content() != 'UKRAINE':
				self.proxies.append('{0}:{1}'.format(p.xpath('td[1]')[0].text_content(), p.xpath('td[2]')[0].text_content()))
		self.counter = 0

	def next_proxy(self):
		if self.counter < len(self.proxies):
			self.counter += 1
			return self.proxies[self.counter-1]
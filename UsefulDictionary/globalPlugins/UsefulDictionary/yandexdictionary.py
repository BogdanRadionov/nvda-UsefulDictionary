#-*- coding:utf-8 -*-

# Copyright (C) 2016 Olexandr Gryshchenko <grisov.dev@mailnull.com>

import addonHandler
addonHandler.initTranslation()

import urllib2
import json

name = _(u'Yandex Dictionary')
url_request = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20160323T212613Z.04d6a10330c1ea29.1553d28e327c7dbf882a82d190e8898ea4313f70&lang={lang}&text={text}'

def sendRequest(text, lang='en-ru'):
   request = json.load(urllib2.urlopen(url_request.format(text=text, lang=lang)))
   return request

def parseResponse(response):
   text = ""
   for elem_key in ["def", "tr", "syn", "mean", "ex"]:
      if response.has_key(elem_key):
         prev_elem = elem_key
         text += {
            "syn":	u"\nсинонимы: ",
            "mean":	u"\nзначение: ",
            "ex":	u"\nнапример: "
            }.get(elem_key, "")
         for elem in response[elem_key]:
            for attr_key in ["text", "pos"]:	# "asp", "num", "gen"
               if elem.has_key(attr_key):
                  if attr_key=="text":
                     text += {
                        "def":	u"\n{}".format(elem[attr_key]),
                        "tr":	u"\n- {}".format(elem[attr_key]),
                        "syn":	u"{}".format(elem[attr_key]),
                        "mean":	u"{}".format(elem[attr_key]),
                        "ex":	u"{}".format(elem[attr_key])
                        }.get(elem_key)
                  if attr_key=="pos":
                     text += " "
                     text += u"({}, {})".format(elem[attr_key], elem["asp"]) if elem.has_key("asp") else u"({})".format(elem[attr_key])
            text += ", " if elem_key==prev_elem else ""
            text += parseResponse(elem)
   return text

def getResult(text, lang, calback):
   result = parseResponse(sendRequest(text, lang))
   calback(result, name)

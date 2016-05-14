#-*- coding:utf-8 -*-

# Copyright (C) 2016 Olexandr Gryshchenko <grisov.dev@mailnull.com>
# Contributor of module Bogdan Radionov <radionov.bogdan@gmail.com>
# API documentation: https://tech.yandex.ru/dictionary/

import addonHandler
addonHandler.initTranslation()

import urllib2
import json

name = _(u'Yandex Dictionary')
key = "dict.1.1.20160323T212613Z.04d6a10330c1ea29.1553d28e327c7dbf882a82d190e8898ea4313f70"
url_request = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=' + key + '&ui=ru&lang={lang}&text={text}'



def sendRequest(text, lang='en-ru'):
   request = json.load(urllib2.urlopen(url_request.format(text=text.encode('utf-8'), lang=lang)))
   return request

def getAttributes(dictElem):
   if not isinstance(dictElem, dict):
      return ""
   attrs = []
   for key in ["pos", "asp", "num", "gen"]:
      if dictElem.has_key(key):
         field = {
            "num":	u"<i>number</i>: ",
            "gen":	u"<i>gender</i>: "
         }.get(key, "") + dictElem.get(key)
         attrs.append(field)
   if len(attrs) > 0:
      result = u" ({})".format( u", ".join(attrs) )
      del attrs
      return result
   return ""

def parseResponse(response):
   text = '''<style>
h1 {
margin:0;
font-family:Verdena, Arial Black, Helvetica, sans-serif;
font-size:22px;
font-weight:bold;
text-decoration:none;
text-align:left;
}
ul {
list-style:square;
}
li {
font-size:16px;
text-decoration:none;
}
p {
font-size:16px;
text-decoration:none;
}
</style>'''
   for key in ["def", "tr", "mean", "syn", "ex"]:
      if response.has_key(key):
         text += {
            "mean":	u"<p><i>Mean</i>: ",
            "syn":	u"<p><i>Synonyms</i>: ",
            "ex":	u"<p><i>Examples</i>: "
         }.get(key, "")
         if key == "def":
            if len(response.get("def"))==0:
               text += u"<h1>no_results</h1>"
            for elem in response.get("def"):
               text += "<h1>" + elem.get("text") + getAttributes(elem) + "</h1>\n"
               text += parseResponse(elem)
               text += "\n"
         if key == "tr":
            text += "<ul>"
            for elem in response.get("tr"):
               text += "<li><b>" + elem.get("text") + "</b>" + getAttributes(elem) + "\n"
               text += parseResponse(elem)
               text += "</li>\n";
            text += "</ul\n>"
         if key == "mean":
            means = []
            for elem in response.get("mean"):
               means.append( elem.get("text") + getAttributes(elem) )
            else:
               if len(means) > 0:
                  text += u", ".join(means) + "</p>\n"
                  del(means)
               text += parseResponse(elem)
         if key == "syn":
            syns = []
            for elem in response.get("syn"):
               syns.append( elem.get("text") + getAttributes(elem) )
            else:
               if len(syns) > 0:
                  text += u", ".join(syns) + "</p>\n"
                  del(syns)
               text += parseResponse(elem)
         if key == "ex":
            exs = []
            for elem in response.get("ex"):
               tmp = elem.get("text") + getAttributes(elem)
               if elem.has_key("tr"):
                  trs = []
                  for extr in elem.get("tr"):
                     trs.append(extr.get("text") + getAttributes(extr))
                  else:
                     if len(trs) > 0:
                        tmp += u" - " + u", ".join(trs)
                        del(trs)
               exs.append(tmp)
            else:
               if len(exs) > 0:
                  text += u", ".join(exs) + "</p>\n"
                  del(exs)
   return text

def getResult(text, lang, calback):
   result = parseResponse(sendRequest(text, lang))
   calback(result, name, True)

#-*- coding:utf-8 -*-

# Copyright (C) 2016 Bogdan Radionov <radionov.bogdan@gmail.com>

import os
import json

name_config = 'config.cfg'
dir_config = os.path.dirname(__file__)

_conf = {}

def load_config():
	global _conf
	_conf = json.load(open(os.path.join(dir_config, name_config)))

load_config()
	
def save_config():
	json.dump(_conf, open(os.path.join(dir_config, name_config), 'w'), indent=4)

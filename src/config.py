#!/usr/bin/env python
# -*- coding=utf-8 -*-

import const
from inifile import IniFile

class Config(IniFile):
	def __init__(self):
		IniFile.__init__(self, const.CONFIG_FILE)
		
		self.login_states = ('10', '20', '30', '40', '50', '60', '70')
		self.login_states_dict = {'10': 0, '20': 1, '30': 2, '40': 3, '50': 4, '60': 5, '70': 6}
		
		self.login_auto_run = self.get_value('login_auto_run')
		self.login_password = self.get_value('login_password')
		self.login_status = self.get_value('login_status')
		self.proxy_enable = self.get_value('proxy_enable')
		self.proxy_uri = self.get_value('proxy_uri')
		self.hot_key = self.get_value('hot_key')
		self.save_path = self.get_value('save_path')
	
	def save(self):
		self.set_value('login_auto_run', self.login_auto_run)
		self.set_value('login_password', self.login_password)
		self.set_value('login_status', self.login_status)
		self.set_value('proxy_enable', self.proxy_enable)
		self.set_value('proxy_uri', self.proxy_uri)
		self.set_value('hot_key', self.hot_key)
		self.set_value('save_path', self.save_path)
		self.write(const.CONFIG_FILE)
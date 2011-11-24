#!/usr/bin/env python
# -*- coding=utf-8 -*-

import gtk, keybinder, appindicator
import const, utils
from configwindow import ConfigWindow

class Tray():
	def __init__(self, window, webview, config):
		self.window = window
		self.webview = webview
		self.config = config
		self.blinking = False
		
		self.tray = appindicator.Indicator("example-simple-client", "QQ", appindicator.CATEGORY_APPLICATION_STATUS)
		self.tray.set_status(appindicator.STATUS_ACTIVE)
		self.iconChange('QQ.png')
		
		menu = gtk.Menu()
		item1 = gtk.MenuItem('显示/隐藏窗口')
		item1.connect("activate", self.click_tray)
		menu.append(item1)
		item2 = gtk.MenuItem('配置...')
		item2.connect("activate", self.click_config)
		menu.append(item2)
		item3 = gtk.ImageMenuItem(gtk.STOCK_QUIT)		
		item3.set_label('退出')
		item3.connect("activate", gtk.main_quit)
		menu.append(item3)
		menu.show_all()
		self.tray.set_menu(menu)
		
		self.webview.connect('title-changed', self.title_changed)
		keybinder.bind(self.config.hot_key, self.keybind_callback)
		
	def iconChange(self, name):
		self.tray.set_icon(const.CURRENT_PATH + name)

	def title_changed(self, view, frame, title):
		windowtitle = self.window.get_title()
		if not title.startswith(const.INIIAL_TITLE) and not utils.same_title(windowtitle, title):
			utils.notification("有新消息来了", title)
			self.iconChange('QQ1.png')
			self.blinking = True
		if title.startswith(const.INIIAL_TITLE):
			self.iconChange('QQ.png')
			self.blinking = False
		self.window.set_title(title)

	def keybind_callback(self):
		self.show_or_hide()

	def click_tray(self, widget):
		self.show_or_hide()

	def click_config(self, widget):
		ConfigWindow(self.webview, self, self.config)

	def show_or_hide(self):
		if self.window.is_active():
			self.window.hide()
		else:
			if self.blinking:
				self.iconChange('QQ.png')
				self.blinking = False
			self.window.present()

#!/usr/bin/env python
# -*- coding=utf-8 -*-

import gtk, keybinder
import const, utils
from configwindow import ConfigWindow

class Tray():
	def __init__(self, window, webview, config):
		self.window = window
		self.webview = webview
		self.config = config
		self.blinking = False
		self.tray = gtk.StatusIcon()
		self.tray.set_from_file(const.ICON)
		self.tray.set_tooltip(const.NAME + ' ' + const.VERSION)
		self.tray.connect('activate', self.click_tray)
		self.tray.connect('popup-menu', self.popup)
		self.webview.connect('title-changed', self.title_changed)
		keybinder.bind(self.config.hot_key, self.keybind_callback)

	def title_changed(self, view, frame, title):
		windowtitle = self.window.get_title()
		if not title.startswith(const.INIIAL_TITLE) and not utils.same_title(windowtitle, title):
			self.tray.set_blinking(True)
			self.blinking = True
			utils.notification("有新消息来了", title)
		if title.startswith(const.INIIAL_TITLE):
			self.tray.set_blinking(False)
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
				self.tray.set_blinking(False)
				self.blinking = False
			self.window.present()

	def popup(self, statusicon, button, activate_time):
		pop_menu = gtk.Menu()
		item1 = gtk.MenuItem('显示/隐藏窗口')
		item1.connect("activate", self.click_tray)
		pop_menu.append(item1)
		
		item2 = gtk.MenuItem('配置...')
		item2.connect("activate", self.click_config)
		pop_menu.append(item2)

		item3 = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		item3.set_label('退出')
		item3.connect("activate", gtk.main_quit)
		pop_menu.append(item3)
		
		pop_menu.show_all()
		pop_menu.popup(None, None, None, 0, gtk.get_current_event_time())

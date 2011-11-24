#!/usr/bin/env python
# -*- coding=utf-8 -*-

import gtk
import const

class MainWindow(gtk.Window):
	def __init__(self, webview, config):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_icon_from_file(const.ICON)
		self.set_default_size(900, 600)
		self.set_title(const.INIIAL_TITLE)
		self.webview = webview
		self.add(self.webview)
		self.webview.open(const.URL)
		self.connect("delete_event", self.minimize)
		self.connect('check-resize', self.check_resize)
		self.set_position(gtk.WIN_POS_CENTER)
		self.show_all()

	def check_resize(self, window):
		self.set_size_request(900, 600)

	def minimize(self, widget, event, data = None):
		self.hide()
		return True

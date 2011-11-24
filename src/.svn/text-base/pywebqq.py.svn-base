#!/usr/bin/env python
# -*- coding=utf-8 -*-

import gtk
import utils

from webqqview import WebQQView
from mainwindow import MainWindow
from config import Config
		
class WebQQ():
	def __init__(self):
		config = Config()
		self.webview = WebQQView(config)
		self.window = MainWindow(self.webview, config)
		
		tray = __import__("tray", fromlist = ['*'])
		if utils.is_unity():
			tray = __import__("unitytray", fromlist = ['*'])
		
		self.tray = tray.Tray(self.window, self.webview, config)

if __name__ == '__main__':
	WebQQ()
	gtk.main()

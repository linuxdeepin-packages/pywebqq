#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os, webkit, ctypes, webbrowser
import const, utils

try:
	libwebkit = ctypes.CDLL('libwebkitgtk-1.0.so.0')
except:
	try:
		libwebkit = ctypes.CDLL('libwebkit-1.0.so.2')
	except:
		libwebkit = ctypes.CDLL('libwebkitgtk-1.0.so')
	
libgobject = ctypes.CDLL('libgobject-2.0.so.0')
libsoup = ctypes.CDLL('libsoup-2.4.so.1')

class WebQQView(webkit.WebView):
	def __init__(self, config):
		webkit.WebView.__init__(self)
		self.hovered_uri = None
		self.config = config
		if self.config.save_path == '':
			self.config.save_path = utils.get_user_download_dir()
		self.init_settings()
		self.init_cookie()
		self.init_proxy()
		self.init_signals()
		
	def init_settings(self):
		settings = self.get_settings()
		settings.set_property("auto-resize-window", False)
		settings.set_property('enable-universal-access-from-file-uris', True)
		settings.set_property('enable-file-access-from-file-uris', True)
		settings.set_property('enable-page-cache', True)
		settings.set_property('enable-spatial-navigation', True)
		settings.set_property('enable-site-specific-quirks', True)
		#settings.set_property('user-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.4+ (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.4+')

	def init_cookie(self):
		if not os.path.exists(const.COOKIE_PATH):
			os.mkdir(const.COOKIE_PATH)
		if not os.path.exists(const.COOKIE_FILE):
			os.mknod(const.COOKIE_FILE)
		session = libwebkit.webkit_get_default_session()
		libgobject.g_object_set(session, 'add-feature', libsoup.soup_cookie_jar_text_new(const.COOKIE_FILE, False), None)
		
	def init_proxy(self):
		if self.config.proxy_enable == 'yes':
			session = libwebkit.webkit_get_default_session()
			libgobject.g_object_set(session, 'proxy-uri', self.config.proxy_uri, None)

	def init_signals(self):
		self.connect('mime-type-policy-decision-requested', self.policy_decision_requested)
		self.connect('download-requested', self.download_requested)
		self.connect("create-web-view", self.create_webView)
		self.connect("hovering-over-link", self.hovering_over_ink)
		self.connect("navigation-policy-decision-requested", self.navigation_policy_decision_requested)
		self.connect("load-finished", self.load_finished)
		
	def load_finished(self, view, frame):
		#print view.get_property('uri') + ':ok:' + frame.get_property('uri')
		frame_uri = frame.get_property('uri')
		if self.config.login_auto_run == 'yes' and const.URL == frame_uri:
			self.execute_script('alloy.portal.runApp(50);')
			return
		
		if utils.is_qq_login(frame_uri):
			self.execute_script("document.getElementById('ifram_login').contentWindow.document.getElementById('p').value='" + self.config.login_password + "';")
			self.execute_script("document.getElementById('ifram_login').contentWindow.onStateItemClick(" + self.config.login_status + ");")
			#if self.login_password != '':
			#	self.execute_script("document.getElementById('ifram_login').contentWindow.document.getElementById('loginform').submit();")

	def navigation_policy_decision_requested(self, view, frame, request, aciton, decision):
		if utils.is_qq_download(request.get_uri()):
			decision.download()
			return True
		return False

	def policy_decision_requested(self, view, frame, request, mimetype, decision):
		if self.can_show_mime_type(mimetype):
			return False
		decision.download()
		return True

	def download_requested(self, view, download):
		download.connect('notify::status', self.download_status)
		download.set_destination_uri('file://' + self.config.save_path + '/' + download.get_suggested_filename())
		return True

	def download_status(self, download, pspec):
		if download.get_status() == -1:
			utils.notification("文件下载失败", self.config.save_path + '/' + download.get_suggested_filename())
		if download.get_status() == 1:
			utils.notification("文件开始下载", self.config.save_path + '/' + download.get_suggested_filename())
		if download.get_status() == 3:
			utils.notification("文件下载完成", self.config.save_path + '/' + download.get_suggested_filename())

	def create_webView(self, view, frame):
		if self.hovered_uri:
			webbrowser.open_new_tab(self.hovered_uri)

	def hovering_over_ink(self, view, title, uri):
		self.hovered_uri = uri

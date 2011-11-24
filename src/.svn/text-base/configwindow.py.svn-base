#!/usr/bin/env python
# -*- coding=utf-8 -*-

import gtk.glade, keybinder
import const, utils
from widgets import KeyGrabber, KeyModifier

class ConfigWindow:
	def __init__(self, webview, tray, config):
		self.webview = webview
		self.tray = tray
		self.config = config
		self.xml = gtk.glade.XML(const.CURRENT_PATH + 'config.glade')
		
		self.cbtnAutoLogin = self.xml.get_widget('cbtnAutoLogin')
		self.cbtnAutoLogin.set_active(self.config.login_auto_run == 'yes')
		self.cbtnAutoLogin.connect("toggled", self.auto_login_toggled)
		
		self.cbtnEnableProxy = self.xml.get_widget('cbtnEnableProxy')
		self.cbtnEnableProxy.set_active(self.config.proxy_enable == 'yes')
		self.cbtnEnableProxy.connect("toggled", self.enable_proxy_toggled)
		
		self.txtPassword = self.xml.get_widget('txtPassword')
		self.txtPassword.set_text(self.config.login_password)
		
		self.txtProxyUri = self.xml.get_widget('txtProxyUri')
		self.txtProxyUri.set_text(self.config.proxy_uri)
		
		self.cbxStatus = self.xml.get_widget('cbxStatus')
		self.cbxStatus.set_active(self.config.login_states_dict[self.config.login_status])
		self.cbxStatus.connect('changed', self.status_changed)
		
		self.txtHotkey = self.xml.get_widget('txtHotkey')
		self.txtHotkey.set_text(self.config.hot_key)
		self.txtHotkey.connect("button-release-event", self.hot_key_clicked)
		
		self.dcbtnSavePath = self.xml.get_widget('dcbtnSavePath')
		self.dcbtnSavePath.set_current_folder(self.config.save_path)
		
		self.btnSave = self.xml.get_widget('btnSave')
		self.btnSave.connect("clicked", self.btnsave_clicked)
		self.btnCancle = self.xml.get_widget('btnCancle')
		self.btnCancle.connect("clicked", self.btncancle_clicked)
		
		self.window = self.xml.get_widget('winConfig')
		self.window.set_icon_from_file(const.ICON)
		self.window.show_all()
		
	def auto_login_toggled(self, widget):
		self.config.login_auto_run = (self.cbtnAutoLogin.get_active() and ['yes'] or ['no'])[0]
		
	def enable_proxy_toggled(self, widget):
		self.config.proxy_enable = (self.cbtnEnableProxy.get_active() and ['yes'] or ['no'])[0]
		
	def status_changed(self, widget):
		self.config.login_status = self.config.login_states[self.cbxStatus.get_active()]

	def hot_key_clicked(self, widget, signal_id):
		grabber = KeyGrabber(self.window.get_toplevel(), label = "Grab key combination")
		grabber.hide()
		grabber.set_no_show_all(True)
		grabber.connect('changed', self.on_got_key)
		grabber.begin_key_grab(None)
		
	def on_got_key(self, widget, key, mods):
		new = gtk.accelerator_name(key, mods)
		for mod in KeyModifier:
			if "%s_L" % mod in new:
				new = new.replace ("%s_L" % mod, "<%s>" % mod)
			if "%s_R" % mod in new:
				new = new.replace ("%s_R" % mod, "<%s>" % mod)
		widget.destroy()
		self.txtHotkey.set_text(new)

	def btnsave_clicked(self, widget):
		self.config.login_password = self.txtPassword.get_text()
		self.config.proxy_uri = self.txtProxyUri.get_text()
		self.config.save_path = self.dcbtnSavePath.get_current_folder()
		try:
			keybinder.unbind(self.config.hot_key)
		except:
			pass
		self.config.hot_key = self.txtHotkey.get_text()
		keybinder.bind(self.config.hot_key, self.tray.keybind_callback)
		self.webview.init_proxy()
		self.config.save()
		utils.notification('保存配置成功', '部分配置重启程序后生效')
		self.window.destroy()

	def btncancle_clicked(self, widget):
		self.window.destroy()

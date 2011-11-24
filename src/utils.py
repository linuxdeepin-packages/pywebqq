#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pynotify, re, os
import const
from inifile import IniFile

QQ_DOWNLOAD_PATTERN = re.compile('http://file[\d]+.web.qq.com/v[\d]+/[\d]+/[\d]+/[\d]+/[\d]+/[\d]+/[\d]+/[\d]+/[\d]+/f/')
QQ_LOGIN_PATTERN = re.compile('http://ui.ptlogin[\d]+.qq.com/cgi-bin/login')

def notification(content, title):
	pynotify.init(const.INIIAL_TITLE)
	notify = pynotify.Notification(content, title, const.ICON)
	notify.set_urgency(pynotify.URGENCY_NORMAL)
	notify.set_timeout(1)
	notify.show()

def same_title(t1, t2):
	t1 = t1.decode("utf-8").replace(" ", "")
	t2 = t2.decode("utf-8").replace(" ", "")
	l = len(t1)
	if l != len(t2):
		return False
	for i in range(l):
		if t1 == shift_string(t2, i):
			return True
	return False

def shift_string(string, i):
	return string[i:] + string[:i]

def is_unity():
	return os.getenv('DESKTOP_SESSION').startswith('ubuntu')

def is_qq_download(uri):
	return QQ_DOWNLOAD_PATTERN.match(uri) != None

def is_qq_login(uri):
	return QQ_LOGIN_PATTERN.match(uri) != None

def get_user_download_dir():
	user_dir_file = IniFile(os.path.join(os.path.expanduser("~"), ".config/user-dirs.dirs"))
	download_dir_val = user_dir_file.get_value('XDG_DOWNLOAD_DIR')
	prefix = download_dir_val.strip('"').split("/")[0]
	if prefix:
		return os.getenv("HOME") + "/" + "/".join(download_dir_val.strip('"').split("/")[1:])
	return download_dir_val.strip('"')

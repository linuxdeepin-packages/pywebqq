#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os.path
import codecs

class IniFile:
    filename = ''

    def __init__(self, filename=None):
        self.content = dict()
        if filename:
            self.parse(filename)

    def parse(self, filename):
        # for performance reasons
        content = self.content

        if not os.path.isfile(filename):
            return

        # parse file
        try:
            file(filename, 'r')
        except IOError:
            return

        for line in file(filename,'r'):
            line = line.strip()
            # empty line
            if not line:
                continue
            # comment
            elif line[0] == '#':
                continue
            # key
            else:
                index = line.find("=")
                key = line[0:index].strip()
                value = line[index+1:].strip()
                if self.has_key(key):
                    continue
                else:
                    content[key] = value

        self.filename = filename

    def get_value(self, key):
        if key not in self.content.keys():
            self.set_value(key, "")
        return self.content[key]

    def write(self, filename = None):
        if not filename and not self.filename:
            return

        if filename:
            self.filename = filename
        else:
            filename = self.filename

        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        fp = codecs.open(filename, 'w')
        for (key, value) in self.content.items():
            fp.write("%s=%s\n" % (key, value))
        fp.write("\n")

    def set_value(self, key, value):
        self.content[key] = value

    def remove_key(self, key):
        for (name) in self.content.items():
            if key == name:
                del self.content[name]

    def has_key(self, key):
        if self.content.has_key(key):
            return True
        else:
            return False

    def get_filename(self):
        return self.filename

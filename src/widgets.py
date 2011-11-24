#!/usr/bin/env python
# -*- coding=utf-8 -*-

import gtk
import gobject
import time

"""Popup and KeyGrabber come from ccsm"""
KeyModifier = ["Shift", "Control", "Mod1", "Mod2", "Mod3", "Mod4", "Mod5", "Alt", "Meta", "Super", "Hyper", "ModeSwitch"]

class Popup(gtk.Window):
    def __init__(self, parent, text=None, child=None, decorated=True, mouse=False, modal=True):
        gtk.Window.__init__ (self, gtk.WINDOW_TOPLEVEL)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        self.set_position(mouse and gtk.WIN_POS_MOUSE or gtk.WIN_POS_CENTER_ALWAYS)
        if parent:
            self.set_transient_for(parent.get_toplevel())
        self.set_modal(modal)
        self.set_decorated(decorated)
        self.set_title("")
        if text:
            label = gtk.Label(text)
            align = gtk.Alignment()
            align.set_padding(20, 20, 20, 20)
            align.add(label)
            self.add(align)
        elif child:
            self.add(child)
        while gtk.events_pending():
            gtk.main_iteration()


    def destroy(self):
        gtk.Window.destroy(self)
        while gtk.events_pending():
            gtk.main_iteration()

class KeyGrabber(gtk.Button):
    __gsignals__ = {
				    "changed" : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [gobject.TYPE_INT, gobject.TYPE_INT]),
                    "current-changed" : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [gobject.TYPE_INT, gobject.TYPE_INT])
                   }

    key     = 0
    mods    = 0
    handler = None
    popup   = None

    label   = None

    def __init__(self, parent = None, key = 0, mods = 0, label = None):
        '''Prepare widget'''
        super (KeyGrabber, self).__init__ ()

        self.main_window = parent
        self.key = key
        self.mods = mods

        self.label = label

        self.connect ("clicked", self.begin_key_grab)
        self.set_label ()

    def begin_key_grab (self, widget):
        self.add_events (gtk.gdk.KEY_PRESS_MASK)
        self.popup = Popup (self.main_window, "请按下您的新组合键")
        self.popup.show_all()
        self.handler = self.popup.connect("key-press-event", self.on_key_press_event)
        while gtk.gdk.keyboard_grab(self.popup.window) != gtk.gdk.GRAB_SUCCESS:
            time.sleep (0.1)

    def end_key_grab (self):
        gtk.gdk.keyboard_ungrab(gtk.get_current_event_time ())
        self.popup.disconnect (self.handler)
        self.popup.destroy ()

    def on_key_press_event (self, widget, event):
        mods = event.state & gtk.accelerator_get_default_mod_mask ()

        if event.keyval in (gtk.keysyms.Escape, gtk.keysyms.Return) \
            and not mods:
            if event.keyval == gtk.keysyms.Escape:
                self.emit ("changed", self.key, self.mods)
            self.end_key_grab ()
            self.set_label ()
            return

        key = gtk.gdk.keyval_to_lower(event.keyval)
        if (key == gtk.keysyms.ISO_Left_Tab):
            key = gtk.keysyms.Tab

        if gtk.accelerator_valid (key, mods) \
            or (key == gtk.keysyms.Tab and mods):
            self.set_label (key, mods)
            self.end_key_grab ()
            self.key = key
            self.mods = mods
            self.emit ("changed", self.key, self.mods)
            return

        self.set_label (key, mods)

    def set_label (self, key = None, mods = None):
        if self.label:
            if key != None and mods != None:
                self.emit ("current-changed", key, mods)
            gtk.Button.set_label (self, self.label)
            return
        if key == None and mods == None:
            key = self.key
            mods = self.mods
        label = gtk.accelerator_name (key, mods)
        if not len (label):
            label = _("Disabled")
        gtk.Button.set_label (self, label)
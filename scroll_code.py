#!/usr/bin/python

from gi.repository import Gtk, GObject, Gdk, Pango
import os
from os import path

class CodeScroll(Gtk.Window):
    black = Gdk.RGBA.from_color(Gdk.color_parse("#000"))
    green = Gdk.RGBA.from_color(Gdk.color_parse("#0F0"))
    # the number of lines to skip
    skip = 30
    # the number of lines to show at a time
    count = 30
    # millis between frames
    speed=50

    def __init__(self, code_dir):
        self.load_codes(code_dir)
        Gtk.Window.__init__(self, title = "Hack the planet")

        self.override_background_color(0, self.black)
        self.override_color(0, self.green)
        self.override_font()
        self.modify_font(Pango.FontDescription('Mono 38'))
        self.text = Gtk.Label("a bunch of code goes here", xalign=0, yalign=0)
        self.add(self.text)
        self.timeout_id = GObject.timeout_add(self.speed, self.scroll_text)
        #self.fullscreen()

    def load_codes(self, code_dir):
        code_files = [ f for f in os.listdir(code_dir) if not f.startswith('.') and path.isfile(path.join(code_dir,f)) ]
        self.codes = {}
        self.code_files = code_files

        for code_file in code_files:
            with open(path.join(code_dir,code_file)) as source:
                self.codes[code_file] = source.readlines()

    def set_code(self, code):
        self.current_code = self.codes[code]
        self.current_code_key = code
        self.top = 0

    def scroll_text(self):
        text = "".join(self.current_code[self.top:self.top + self.count])
        max_size = len(self.current_code)
        overflow = max_size - self.top
        if overflow < self.count:
            print overflow
            text += "".join(self.current_code[0:self.count-overflow])
        self.text.set_text(text)
        self.top = (self.top + self.skip) % (len(self.current_code))

        return True

    def next_code(self):
        cur_idx = self.code_files.index(self.current_code_key)
        next_idx = (cur_idx + 1) % len(self.code_files)
        self.set_code(self.code_files[next_idx])

    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_space:
            self.next_code()


win = CodeScroll("/home/steve/work/projects/hacker_photobooth/codes")
win.set_code('hy')
win.connect("delete-event", Gtk.main_quit)
win.connect("key-press-event", win.on_key_press_event)
win.show_all()
cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
win.get_window().set_cursor(cursor)
Gtk.main()
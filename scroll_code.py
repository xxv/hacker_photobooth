#!/usr/bin/python

from gi.repository import Gtk, GObject, Gdk, Pango
import os
from os import path

class CodeScroll(Gtk.Window):
    black = Gdk.RGBA.from_color(Gdk.color_parse("#000"))
    green = Gdk.RGBA.from_color(Gdk.color_parse("#0F0"))
    red = Gdk.RGBA.from_color(Gdk.color_parse("#F00"))
    # the number of lines to skip
    skip = 30
    # the number of lines to show at a time
    count = 30
    # millis between frames
    speed=50

    blank_id = None

    green_brightness = 10

    def __init__(self, code_dir):
        self.load_codes(code_dir)
        Gtk.Window.__init__(self, title = "Hack the planet")

        self.override_background_color(0, self.black)
        self.override_color(0, self.green)
        self.modify_font(Pango.FontDescription('Mono 38'))

        fixed = Gtk.Overlay()
        self.text = Gtk.Label("", xalign=0, yalign=0)
        fixed.add_overlay(self.text)

        lang = Gtk.Label("")
        lang.override_color(0, self.red)
        lang.set_justify(Gtk.Justification.CENTER)
        lang.modify_font(Pango.FontDescription('Mono Bold 128'))
        fixed.add_overlay(lang)
        self.language = lang

        self.add(fixed)

        GObject.timeout_add(self.speed, self.scroll_text)

    def load_codes(self, code_dir):
        code_files = [ f for f in os.listdir(code_dir) if not f.startswith('.') and path.isfile(path.join(code_dir,f)) ]
        self.codes = {}
        self.code_files = code_files

        for code_file in code_files:
            with open(path.join(code_dir,code_file)) as source:
                self.codes[code_file] = source.readlines()

    def set_code(self, code):
        if self.blank_id:
            GObject.source_remove(self.blank_id)
        self.current_code = self.codes[code]
        self.current_code_key = code
        self.top = 0
        self.language.set_text(code)
        self.blank_id = GObject.timeout_add(2000, self.hide_language)

    def hide_language(self):
        self.language.set_text("")
        self.blank_id = None
        return False

    def scroll_text(self):
        text = "".join(self.current_code[self.top:self.top + self.count])
        max_size = len(self.current_code)
        overflow = max_size - self.top
        if overflow < self.count:
            text += "".join(self.current_code[0:self.count-overflow])
        self.text.set_text(text)
        self.top = (self.top + self.skip) % (len(self.current_code))

        return True

    def next_code(self):
        cur_idx = self.code_files.index(self.current_code_key)
        next_idx = (cur_idx + 1) % len(self.code_files)
        self.set_code(self.code_files[next_idx])

    def on_key_press_event(self, widget, event):
        v = event.keyval
        if v == Gdk.KEY_space:
            self.next_code()
        elif v == Gdk.KEY_minus:
            self.dim_text()
        elif v == Gdk.KEY_equal:
            self.brighten_text()
        elif v == Gdk.KEY_F11:
            self.fullscreen()
        elif v == Gdk.KEY_Escape:
            self.unfullscreen()

    def set_text_brightness(self, brightness):
        self.green_brightness = brightness
        self.override_color(0, Gdk.RGBA(0, brightness / 10.0, 0, 1))

    def dim_text(self):
        bright = self.green_brightness
        if bright > 0:
            bright -= 1
        self.set_text_brightness(bright)

    def brighten_text(self):
        bright = self.green_brightness
        if bright < 10:
            bright += 1
        self.set_text_brightness(bright)


win = CodeScroll("/home/steve/work/projects/hacker_photobooth/codes")
win.set_code('hy')
win.connect("delete-event", Gtk.main_quit)
win.connect("key-press-event", win.on_key_press_event)
win.show_all()
cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
win.get_window().set_cursor(cursor)
Gtk.main()

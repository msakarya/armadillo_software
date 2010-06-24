#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import sys
import gtk

class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui.glade")
        self.window = builder.get_object("window1")
        builder.connect_signals(self)

    def on_window1_destroy(self, widget, data=None):
        gtk.main_quit()
    

if __name__=="__main__":
    app=Main()
    app.window.show()    
    gtk.main()

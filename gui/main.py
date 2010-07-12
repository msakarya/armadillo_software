#!/usr/bin/env python
import sys
f=open("debug.txt","w")
class STD:
    def __init__(self):        
        a=0
    def write(self,arg=None):
        f.write(arg)  
        
debug=False
if debug:
    sys.stderr=STD()
    sys.stdout=sys.stderr

import pygtk
pygtk.require("2.0")
import sys
import gtk

class Main:
    def __init__(self):        
        builder = gtk.Builder()                 
        builder.add_from_file("gui.glade")
        self.window = builder.get_object("window1")
        self.about = builder.get_object("aboutdialog1")
        builder.connect_signals(self)  
        print("selam")
    def on_window1_destroy(self, widget, data=None):
        gtk.main_quit()
    def on_aboutdialog1_show(self, widget, data=None):
        self.about.show()
    def on_aboutdialog1_response(self, widget, data=None):        
        self.about.hide()    

if __name__=="__main__":
    app=Main()   
    app.window.show()
    gtk.main()

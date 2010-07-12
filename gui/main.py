#!/usr/bin/env python
import sys

debug_file="debug.txt"
glade_file="gui.glade"

class STD:
    def __init__(self,file):
        self.file=file
    def write(self,arg=None):
        self.file.write(arg)
        sys.__stdout__.write(arg)        
        
mod="normal"
if mod=="debug":    
    f=open(debug_file,"w")
    sys.stdout=STD(f)
    sys.stderr=sys.stdout

import pygtk
pygtk.require("2.0")
import sys
import gtk

from com import COM

class Main:
    def __init__(self):        
        builder = gtk.Builder()                 
        builder.add_from_file(glade_file)
        self.window = builder.get_object("window1")
        self.about = builder.get_object("aboutdialog1")
        self.tbconnect=builder.get_object("tbconnect")
        builder.connect_signals(self)

        self.com=COM()
        self.tbconnect.set_active(True)        
    def on_btsend_clicked(self, widget, data=None):
        self.com.write([1,2,3])
    def on_tbconnect_clicked(self, widget, data=None):
        if widget.get_active():            
            self.com.connect()
            widget.set_label("Connected")
        else:                  
            self.com.disconnect()
            widget.set_label("      Closed")       
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

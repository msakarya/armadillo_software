#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import sys
import gtk

from com import COM

class Main:
    def __init__(self):        
        builder = gtk.Builder()                 
        builder.add_from_file(conf.d['glade_file'])
        self.window = builder.get_object("window1")
        self.about = builder.get_object("aboutdialog1")
        self.tbconnect=builder.get_object("tbconnect")
        self.preferences_dialog=builder.get_object("preferences_dialog")
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
    def on_preferences_dialog_show(self, widget, data=None):
        for item in conf.d:
            print(item,conf.d[item])
        self.preferences_dialog.show()    
    def on_bt_preferences_dialog_new_clicked(self, widget, data=None):
        print(data)
    def on_bt_preferences_dialog_save_clicked(self, widget, data=None):
        self.preferences_dialog.hide()
    def on_bt_preferences_dialog_cancel_clicked(self, widget, data=None):
        self.preferences_dialog.hide()
    def on_window1_destroy(self, widget, data=None):
        gtk.main_quit()
    def on_aboutdialog1_show(self, widget, data=None):
        self.about.show()
    def on_aboutdialog1_response(self, widget, data=None):        
        self.about.hide()
        
class Preferences:
    def __init__(self,parent=None):
        self.parent=parent

class STD:
    def __init__(self,file):
        self.file=file
    def write(self,arg=None):
        self.file.write(arg)
        sys.__stdout__.write(arg)

class Configure:
    def __init__(self):
        import pickle
        self.p=pickle
        self.load()
        d=self.d
        if d['mod']=="debug":
            f=open(d['debug_file'],"w")
            sys.stdout=STD(f)
            sys.stderr=sys.stdout
    def load(self):        
        pickle=self.p
        fpickle=open('config.pickle','r')
        self.d=pickle.load(fpickle) # Dictionary
        fpickle.close()
    def save(self):
        pickle=self.p
        fpickle=open('config.pickle','w')
        pickle.dump(self.d, fpickle) # Dictionary
        fpickle.close()

conf=Configure()

if __name__=="__main__":
    app=Main()   
    app.window.show()
    gtk.main()

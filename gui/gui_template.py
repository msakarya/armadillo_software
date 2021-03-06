#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'
import pygtk
pygtk.require("2.0")
import sys
import os
import gtk

class MainWindow:
    def __init__(self):        
        builder = gtk.Builder()
        self.builder=builder
        f='glade'+os.sep+conf.d['glade_file']
        builder.add_from_file(f)
        self.window = builder.get_object("window1")
        self.about = builder.get_object("aboutdialog1")
        self.tbconnect=builder.get_object("tbconnect")
        self.preferences_dialog=builder.get_object("preferences_dialog")
        self.preferences_dialog_align= builder.get_object("preferences_dialog_vbox")
        self.pd_entry=builder.get_object("pd_entry")
        self.pd_cb=builder.get_object("pd_cb")
        self.pd_cb_liststore=builder.get_object("pd_cb_liststore")        
        self.statusbar=builder.get_object("statusbar1")          
        builder.connect_signals(self)            
        self.pd_init()          
    def on_tbconnect_clicked(self, widget, data=None):
        if widget.get_active():          
            widget.set_label("Connected")
        else:                              
            widget.set_label("      Closed")
    def on_pd_cb_changed(self, widget, data=None):
        entry=self.pd_entry #Preferences dialog combobox
        cb=self.pd_cb
        active=cb.get_active_text()
        entry.set_text(conf.d[active])
    def pd_init(self):
        cb=self.pd_cb   #Fill in preferences dialog
        liststore = self.pd_cb_liststore
        for item in conf.d:
            liststore.append([item])
        cb.set_model(liststore)        
        cb.set_text_column(0)
        cb.set_active(0)
    def on_preferences_dialog_show(self, widget, data=None):     
        self.preferences_dialog.show()        
    def on_pd_set_bt_clicked(self, widget, data=None):        
        entry=self.pd_entry
        cb=self.pd_cb
        active=cb.get_active_text()
        conf.d[active]=entry.get_text()
        conf.save()
    def on_pd_close_bt_clicked(self, widget, data=None):
        self.preferences_dialog.hide()
    def on_window1_destroy(self, widget, data=None):                  
        gtk.main_quit()
    def on_aboutdialog1_show(self, widget, data=None):
        self.about.show()
    def on_aboutdialog1_response(self, widget, data=None):        
        self.about.hide()
        
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
        #self.d['newitem']='newvalue'
        pickle.dump(self.d, fpickle) # Dictionary
        fpickle.close()        

conf=Configure()

if __name__=="__main__":    
    app=MainWindow()
    app.window.show()       
    gtk.main()    
    

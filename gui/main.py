#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import sys
import gtk
from com import COM
import re

class Main:
    def __init__(self):        
        builder = gtk.Builder()                 
        builder.add_from_file(conf.d['glade_file'])
        self.window = builder.get_object("window1")
        self.about = builder.get_object("aboutdialog1")
        self.tbconnect=builder.get_object("tbconnect")
        self.preferences_dialog=builder.get_object("preferences_dialog")
        self.preferences_dialog_align= builder.get_object("preferences_dialog_vbox")
        self.pd_entry=builder.get_object("pd_entry")
        self.pd_cb=builder.get_object("pd_cb")
        self.pd_cb_liststore=builder.get_object("pd_cb_liststore")
        self.l_message=builder.get_object("l_message")
        self.statusbar=builder.get_object("statusbar1")
        self.console_view=builder.get_object("console_view")
        self.console_text=builder.get_object("console_text")
        builder.connect_signals(self)

        self.com=COM(read_cbf=self.read_cbf)
        self.tbconnect.set_active(True)
        self.pd_init()
    def read_cbf(self,data):
        if(data[0]=='s'):
            if(len(data)>12):
                #self.l_message.set_text(''.join(data))
                str=''.join(data)
                str=re.split('[^0-9]', str)                
                self.statusbar.push(0,''.join(str)+' seconds')
        if(data[0]=='$'):
            str=''.join(data)            
            ct=self.console_text
            enditer = ct.get_end_iter()
            ct.insert(enditer, str)
    def on_btsend_clicked(self, widget, data=None):        
        self.com.write("id?\r")
    def on_tbconnect_clicked(self, widget, data=None):
        if widget.get_active():            
            self.com.connect()
            widget.set_label("Connected")
        else:                  
            self.com.disconnect()
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
        try:
            self.com.close()
        except:
            a=0
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
    gtk.gdk.threads_init()
    app=Main()   
    app.window.show()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    #gtk.threads_enter()
    #gtk.threads_leave()

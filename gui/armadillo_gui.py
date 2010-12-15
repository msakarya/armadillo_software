#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'
import pygtk
pygtk.require("2.0")
import sys
import os
"""
pyelectronics_path='/home/mustafa/work/projects/armadillo_software/gui/pyelectronics'
if not os.path.isdir(pyelectronics_path):
    print pyelectronics_path+' not found'
    sys.exit()
sys.path.append(pyelectronics_path)
print sys.path
"""
import gtk
from pyelectronics import Armadillo
from gui_template import MainWindow
from widgets import WPlot
from collections import deque
import gobject

gtk.gdk.threads_init()
class Panel(gtk.VBox):
    def __init__(self,parent,name):
        self.par=parent
        gtk.VBox.__init__(self)
        builder = gtk.Builder()
        self.builder=builder
        f='glade'+os.sep+name+'.glade'
        builder.add_from_file(f)
        self.table = builder.get_object("table1")
        self.table.reparent(self)
        builder.connect_signals(self)
        self.kit=self.par.kit
        self.d=self.kit.d
        self.f=self.kit.f
class Panel1(Panel):
    def __init__(self,parent,name):
        Panel.__init__(self,parent,name)
        builder=self.builder
        self.textview1=builder.get_object("textview1")
        self.textbuffer1=builder.get_object("textbuffer1")
        self.scrolledwindow1=builder.get_object("scrolledwindow1")        
        
        f=self.f
        f['message']=self.console_write
    def console_write(self,data):
        """
        tb=self.textbuffer1
        line_count=tb.get_line_count()
        end_iter = tb.get_end_iter()
        try:
            tb.insert(end_iter, data)
            if(line_count>10):
                start_iter=tb.get_start_iter()
                start_iter2=tb.get_start_iter()
                start_iter2.forward_lines(1)

                tb.delete(start_iter,start_iter2)
        except:
            print("cb error")
        """
        a=0
    def on_button1_clicked(self, widget, data=None):
        self.kit.request_id()
    
class Panel2(Panel):    
    def __init__(self,parent,name):
        Panel.__init__(self,parent,name)        
        f=self.f
        f['adc']=self.fadc
        self.cnt=0
        self.flag=True
        self.fifo=deque()
        self.size=20
        for i in range(self.size):
            self.fifo.appendleft(1023)
        builder=self.builder
        self.label=range(10)
        self.label[0]=builder.get_object('label2')
        self.cb=builder.get_object("cb")
        self.cb_ls=builder.get_object("ls")
        
        self.play_button=builder.get_object('play_button')
        self.plot_layout=builder.get_object('vbox3')
        self.plot=WPlot(self)
        self.plot_layout.pack_start(self.plot, False, False, 0)
        self.cb_init()
        self.t1_enable=True
        gobject.timeout_add(1000, self.t1f)
        self.playing=True
    def t1f(self):
        if(self.t1_enable):
            self.plot.insert(int(100.0*self.kit.adc[7]/1023))
        return True
    def on_cb_changed(self,widget, data=None):
        cb=self.cb
        active=cb.get_active_text()
        print(active)
        self.plot.reset()
    def cb_init(self):
        cb=self.cb   #Fill in preferences dialog
        ls = self.cb_ls
        l=["adc0","adc1","adc2"]
        for item in l:
            ls.append([item])
        cb.set_model(ls)
        cb.set_text_column(0)
        cb.set_active(0)
    def on_play_button_clicked(self, widget, data=None):
        if(self.playing):
            self.playing=False
            self.t1_enable=False
            self.play_button.set_label("paused")
        else:
            self.plot.reset()
            self.playing=True
            self.t1_enable=True
            self.play_button.set_label("playing")
    def fadc(self,data):
        self.cnt=self.cnt+1
        if((self.cnt%25)==10):
            pass
            #print(data[7])
            
class Panel3(Panel):
    def __init__(self,parent,name):
        Panel.__init__(self,parent,name)
        self.tbvals=range(2)
        builder=self.builder
        self.hscale=range(8)
        self.hscale[0]=builder.get_object('hscale1')
        self.cb_liststore=builder.get_object('cb_liststore')
        self.cb2_liststore=builder.get_object('cb2_liststore')
        self.cb=builder.get_object('comboboxentry1')
        self.cb2=builder.get_object('comboboxentry2')
        self.which=0
        adj=range(8)
        for i in range(1):
            adj[i] = gtk.Adjustment(1, 1, 250, 1, 1, 0)
            self.hscale[i].set_adjustment(adj[i])
            self.hscale[i].set_draw_value(True)
            self.hscale[i].set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.cb_init()
        
    def cb_init(self):
        cb=self.cb   #Fill in preferences dialog
        liststore = self.cb_liststore        
        for i in range(4):
            liststore.append([i])
        cb.set_model(liststore)
        cb.set_text_column(0)
        cb.set_active(0)
        cb=self.cb2   #Fill in preferences dialog
        liststore = self.cb2_liststore
        for i in range(8):
            liststore.append([i])
        cb.set_model(liststore)
        cb.set_text_column(0)
        cb.set_active(0)
    def on_cb_changed(self, widget,data=None):
        by=int(self.cb.get_active_text())        
        try:
            bt=int(self.cb2.get_active_text())
        except:
            bt=0
        which=by*8+bt
        k=self.kit
        self.hscale[0].set_value(k.s_pos[which])
        self.which=which
    def on_osf(self):  #one shot function
        self.kit.s_set_value(self.which, self.tbvals[0])
    def on_hscale_change_value(self, widget,data=None,d=None): 
        val=int(widget.get_value())      
        self.tbvals[0]=val
        if not self.on_osf in self.kit.f['osf']:
            self.kit.f['osf'].append(self.on_osf)
        #self.kit.s_set_value(self.which, val)
        """
        futaba s3003 50-230

        """
class Main(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
        builder=self.builder
        self.panel_container=range(3)
        self.panel_container[0]=builder.get_object("vbox1")
        self.panel_container[1]=builder.get_object("vbox2")
        self.panel_container[2]=builder.get_object("vbox3")
        self.kit=Armadillo()
        d=self.kit.d
        f=self.kit.f
        self.panel=range(3)
        self.panel[0]=Panel1(self,'panel1')
        self.panel[1]=Panel2(self,'panel2')
        self.panel[2]=Panel3(self,'panel3')
        
        for i in range(3):
            self.panel_container[i].pack_start(self.panel[i],False,False)
            self.panel_container[i].show_all()
        f['seconds']=self.func_seconds
        self.tbconnect.set_active(True)
    def on_tbconnect_clicked(self, widget, data=None):
        if widget.get_active():            
            self.kit.connect()
            widget.set_label("Connected")
        else:                  
            self.kit.disconnect()
            widget.set_label("      Closed")
    def func_seconds(self,data):
        self.statusbar.push(0,''.join(data)+' seconds')
    def on_window1_destroy(self, widget, data=None):
        self.kit.destroy()
        gtk.main_quit()


if __name__=="__main__":    
    app=Main()
    app.window.show()  
    #gtk.gdk.threads_enter()
    gtk.main()
    #gtk.gdk.threads_leave()

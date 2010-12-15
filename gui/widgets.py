#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'
import pygtk
pygtk.require("2.0")
import os
import gtk
import gobject
from collections import deque

class WidgetBase(gtk.VBox):
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
        

class WPlot(WidgetBase):

    def __init__(self, parent):
        self.t1cnt=0
        name='wplot'
        WidgetBase.__init__(self,parent,name)
        builder=self.builder
        self.da=builder.get_object('drawingarea1')
        plot_h=240
        plot_w=int(plot_h*2.2)
        self.da.set_size_request(plot_w, plot_h)
        self.hruler=builder.get_object('hruler')
        self.vruler=builder.get_object('vruler')
        self.htexts=builder.get_object('htext')
        self.vtexts=builder.get_object('vtext')        

        self.plot_dim=(plot_w,plot_h)

        vstep_count=25
        label_sep_v=plot_h/24.8-0.6
        vrange=[0,100]
        vlabel_step=(vrange[1]-vrange[0])/5
        self.vrange=vrange
        self.vlabel=range(vstep_count+1)
        vlabel_max_len=0
        for i in range(vstep_count/5+1):
            text=str(vlabel_step*i+vrange[0])
            if(vlabel_max_len<len(text)):
                vlabel_max_len=len(text)
        for i in range(vstep_count/5+1):
            text=str(vlabel_step*i+vrange[0])            
            self.vlabel[i]= gtk.Label(text)
            self.vtexts.put(self.vlabel[i],(vlabel_max_len-len(text))*6,
                    int(label_sep_v*(vstep_count-i*5))-5)
        
        hstep_count=60
        label_sep_h=plot_w/30.0-0.6
        hrange=[0,100]
        hlabel_step=(hrange[1]-hrange[0])/10
        self.hstep_count=hstep_count
        self.hrange=hrange
        self.hlabel=range(hstep_count+1)
        hlabel_max_len=0
        
        for i in range(hstep_count/5+1):
            text=str(hlabel_step*i+hrange[0])
            if(hlabel_max_len<len(text)):
                hlabel_max_len=len(text)
        for i in range(hstep_count/10):
            text=str(hlabel_step*i+hrange[0])
            self.hlabel[i]= gtk.Label(text)
            self.htexts.put(self.hlabel[i],
                int(label_sep_h*(i*5)),0)

        gobject.timeout_add(250,self.t1f)
        self.t1enable=True
        self.t1cnt=0        
        self.dq=deque()
        
        self.slide=False
        self.reset_flag=False
       
    def t1f(self):
        if (self.t1enable):           
            self.da.queue_draw()
        return True #False to stop    
    def on_vruler_expose_event(self, widget, event):       
        print event.area
        cr=self.vruler.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()
        cr.set_source_rgb(0.99, 0.99, 0.99)
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.fill()
        height=event.area.height
        width=event.area.width
        
        step_count=25
        hstep=1.0*height/step_count        
        
        cr.set_source_rgb(0.7, 0.7, 0.9)
        cr.set_line_width(1)
        
        for i in range(step_count+1):
            step=i*hstep
            if i%5:
                cr.move_to(2*width / 3, step)
            else:
                cr.move_to(width / 3, step)
            cr.line_to(width, step)
            #cr.fill()
            cr.stroke()
        
        #cr.clip()
    def on_hruler_expose_event(self, widget, event):        
        print event.area
        cr=self.hruler.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()
        cr.set_source_rgb(0.99, 0.99, 0.99)
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.fill()
        
        height=event.area.height
        width=event.area.width

        step_count=60
        hstep=1.0*width/step_count

        cr.set_source_rgb(0.7, 0.7, 0.9)
        cr.set_line_width(1)

        for i in range(step_count):
            step=i*hstep
            if i%10:
                cr.move_to(step,height/3 )
            else:
                cr.move_to(step, 2*height/3)
            cr.line_to(step, 0)
            #cr.fill()
            cr.stroke()
    def on_drawingarea1_expose_event(self, widget, event):       
        cr=self.da.window.cairo_create()
        
        cr.rectangle(event.area.x, event.area.y,
                    event.area.width, event.area.height)
        cr.clip()
        
        self.set_da_scene(cr,event)
        if self.reset_flag:
            self.t1enable=False
            self.reset_flag=False
            for i in range(6):
                self.hlabel[i].set_text(str(i*10))
        else:
            self.line(cr,event)
        
    def insert(self,py):
        dq=self.dq
        plot_w,plot_h=self.plot_dim
        vmin,vmax=self.vrange
        hmin,hmax=self.hrange
        if py<vmin:
            py=vmin
        elif py>vmax:
            py=pmax
        py=int(plot_h-1.0*plot_h/(vmax-vmin)*py)
        px_step=int(4.0*plot_w/(hmax-hmin))

        if(len(dq)>0):
            px=dq[0][0]+px_step
        else:
            px=0
        dq.appendleft((px,py))
        self.t1enable=True
    def reset(self):
        self.reset_flag=True
        self.t1enable=True
        while(len(self.dq)>0):
            self.dq.pop()
    def line(self,cr,event):       
        plot_w=event.area.width
        px_step=1.0*plot_w/self.hstep_count
        
        dq=self.dq
        
        for i in range(len(dq)-1):
            cr.set_source_rgb(0.2, 0.2, 0.7)
            cr.set_line_width(6)
            px,py=dq[-1-i]
            
            px=int(px_step*i)

            cr.rectangle(px-2, py-2,4,4)
            
            cr.fill()
            
            cr.set_source_rgb(0.7, 0.2, 0.2)
            cr.set_line_width(1)
            cr.move_to(px, py)
            px,py=dq[-2-i]
            px=int(px_step*(i+1))
            cr.line_to(px,py)
            cr.stroke()
            
        if self.slide:
            self.slide=False
            for i in range(6):
                s=self.hlabel[i].get_text()
                self.hlabel[i].set_text(str(int(s)+10))
        while(len(dq)>self.hstep_count-1):
            for i in range(10):
                dq.pop()
            self.slide=True
        
        #cr.restore()
        self.t1enable=False
       
    def set_da_scene(self, cr,event):
        
        width,height=self.da.window.get_size()
        cr.set_source_rgb(0.99, 0.99, 0.99)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        
        cr.set_line_width(1)
        cr.set_source_rgb(0.7, 0.7, 0.9)

        hstep_count=60
        hgrid_step=1.0*width/hstep_count
        for i in range(hstep_count+1):
            if (i%5):
                cr.set_source_rgb(0.9, 0.9, 0.98)
            else:
                cr.set_source_rgb(0.7, 0.7, 0.9)
            cr.move_to(int(i*hgrid_step), 0)
            cr.line_to(int(i*hgrid_step), height)
            cr.stroke()

        vstep_count=25
        vgrid_step=1.0*height/vstep_count
        for i in range(vstep_count+1):
            if (i%5):
                cr.set_source_rgb(0.9, 0.9, 0.98)
            else:
                cr.set_source_rgb(0.7, 0.7, 0.9)
            cr.move_to(0, int(i*vgrid_step))
            cr.line_to(width, int(i*vgrid_step))
            cr.stroke()
       
if __name__=="__main__":
    pass
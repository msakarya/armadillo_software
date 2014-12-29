#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'

import re,sys
import urllib
import json
import time
from SocketServer import BaseRequestHandler, TCPServer
import socket
from com import TTimer
import hashlib
        
class Network:   
    def __init__(self,ncbf=None,parent=None):  
        self.parent=parent  
        email="mustafasakarya1986@gmail.com"
        h=hashlib.md5()
        h.update(email.lower())        
        self.webid=h.hexdigest()
        self.dburl="http://electronnics-tinywebdb.appspot.com/"#"http://localhost:8081/"#
        self.dbgeturl=self.dburl+"getvalue"
        self.dbstoreurl=self.dburl+"storeavalue" 
        self.ncbf=ncbf
        self.timer=TTimer(self.t1f,1)
        self.timer.start()  
    def connect(self):
        self.timer.enabled=True
    def disconnect(self):
        self.timer.enabled=False
    def t1f(self,kendi):
        data= self.webdbget("webidtask_"+self.webid)
        if self.ncbf and data:
            self.ncbf(data)        
        kendi.cnt=kendi.cnt+1
        #if kendi.cnt>20:
        #    self.timer.enabled=False
    def network_rcbf(self,data):        
        self.parse(data)
    def parse(self,data):
        webidlist = self.webdbget("webid")
        webidlist = json.loads(webidlist)[2]
        if len(webidlist) > 0:
            webidlist = eval(webidlist)

        if not isinstance(webidlist,list):
            webidlist=[]
            print "webidlist cleared"
        if not self.webid in webidlist:
            webidlist.append(self.webid)
            self.webdbstore("webid",webidlist)
            print "webid is stored"
        else:
            print "webid already available"
    def webdbget(self,tag):
        data = urllib.urlencode({"tag" : tag})
        fwebdb=urllib.urlopen(self.dbgeturl,data)
        swebdb=fwebdb.read()
        fwebdb.close()
        
        datalist = swebdb
        datalist = json.loads(datalist)[2]       
        
        if len(datalist) > 0:
            datalist = eval(datalist)
            return datalist
        else:
            return None           
       
    def webdbstore(self,tag,value):
        data = urllib.urlencode({"tag" : tag,"value":value})
        fwebdb=urllib.urlopen(self.dbstoreurl,data)
        swebdb=fwebdb.read()
        fwebdb.close()
        return swebdb
           
         
    
if __name__ == "__main__":
    n=Network()
    for i in range(5):
        print n.webdbget("webidtask_"+n.webid)
        time.sleep(1)
    #n.connect()
    



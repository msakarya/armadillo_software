#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'

from com import COM,TClient,TServer
import re,sys
import urllib
import json
import time
from SocketServer import BaseRequestHandler, TCPServer
import socket
class ADC:
    def __init__(self):
        self.adc=range(32)
    def parse_adc(self,data):
        if(data[1]=='n'and(len(data)==18)):
            self.adc=range(8)
            adc_temp=bytearray(data[2:])            
            for i in range(8):
                self.adc[i]=adc_temp[i*2]*256+adc_temp[i*2+1]
        if(data[1]=='d'and(len(data)>18)):
            self.adc=range(32)
            adc_temp=bytearray(data[2:])
            for i in range(32):
                self.adc[i]=adc_temp[i*2]*256+adc_temp[i*2+1]
class SERVO:
    def __init__(self):
        self.s_pos=range(32)
        self.s_velocity=range(32)
        for i in range(32):
            self.s_pos[i]=120
            self.s_velocity[i]=0
    def pack_servo(self,which):
        w=which
        l=[]
        l.append(ord('s'))
        l.append(w)
        l.append(self.s_pos[w])
        l.append(self.s_velocity[w])        
        return l
    def s_set_value(self,which,pos,velocity=None):
        w=which
        self.s_pos[w]=pos
        self.s_velocity[w] = velocity if velocity else 0
        l=self.pack_servo(w)
        self.com.write(l)        
        return l
global nparent
nparent=None
class ServerHandler(BaseRequestHandler):
    
    def handle(self):
        global nparent
        
        #print "Client connected:" , self.client_address
        data=self.request.recv(2**16)
        
        l= data.split("\n")
        #print l
        for s in l:
            if s.find("tag")>=0:
                nparent.sh_cbf(s)
        
        self.request.sendall(data)
        self.request.close()
class Network:   
    def __init__(self,parent=None):  
        self.parent=parent  
        self.client=TClient(prc='main')
        self.server=TServer(prc='main',rcbf=self.network_rcbf,ip="85.101.34.130",port=80)
        self.server.start()  
        """ 
        self.webid="armadilloKit1235"
        self.dburl="http://electronnics-tinywebdb.appspot.com/"
        self.dbgeturl=self.dburl+"getvalue"
        self.dbstoreurl=self.dburl+"storeavalue" 
        self.port = "43180"   
        global nparent
        nparent=self
        self.sh=TCPServer(("192.168.1.43",43180),ServerHandler)
        """
    def sh_cbf(self,data):
        data=data.split("=")[2]
        conversion={"%5B":"[","%22":"\"","%5D":"]","%2C":","}
        for key in conversion.keys():
            data=data.replace(key,conversion[key])
            
        tag,value=eval(data)
        print tag,value
        #l=data.split("storeavalue")
        #if len(l)>1:
            #l=l[1].split(",")
        #    print l
            #tag=eval(l[0].split("=")[1])
            #value=eval(l[1].split(" ")[0].split("=")[1])
            #print "tag = ",tag," value = ",value
    def network_rcbf(self,data):        
        self.parse(data)
    def getgip(self):
        fip = urllib.urlopen("http://www.whatismyip.org/")
        sip = fip.read()       
        fip.close()
        return sip
    def webdbget(self,tag):
        data = urllib.urlencode({"tag" : tag})
        fwebdb=urllib.urlopen(self.dbgeturl,data)
        swebdb=fwebdb.read()
        fwebdb.close()
        return swebdb
    def webdbstore(self,tag,value):
        data = urllib.urlencode({"tag" : tag,"value":value})
        fwebdb=urllib.urlopen(self.dbstoreurl,data)
        swebdb=fwebdb.read()
        fwebdb.close()
        return swebdb
    def register(self):
        self.sip=self.getgip()
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
        data=[time.ctime(),self.sip,self.port]
        self.webdbstore("webidip_"+self.webid,data)
        print 'registered'
    def parse(self,data): 
        kit=self.parent  
        print data
        """     
        if isinstance(data,str):
            try:
                exec(data)
            except:
                print "exception"           
        """    
    def write(self,arg):
        self.client.send(arg)
    def kill(self):
        self.server.kill()  
class STD:
    def __init__(self): 
        sys.stdout=self 
        sys.stderr=sys.stdout       
        self.f=[]    
    def write(self,arg=None):
        sys.__stdout__.write(arg)
        for f in self.f:
            f.write(arg)        
        
class Armadillo(ADC,SERVO):
    def __init__(self):
        self.std=STD()        
        ADC.__init__(self)
        SERVO.__init__(self)
        self.com=COM(read_cbf=self.parse)
        
        self.network=Network(parent=self)
        self.std.f.append(self.network)       
        
        self.d={}
        self.f={}
        f=self.f
        d=self.d
        d['request_id']="id?\r"
        f['message']=None
        f['seconds']=None
        f['adc']=None
        f['osf']=[] #one shot functions to be called
                    #at sync with com checkout
        
    def parse(self,data):
        d=self.d
        f=self.f
        if(data[0]=='s'):
            if(len(data)>12):                
                s=''.join(data)
                s=re.split('[^0-9]', s)
                if(f['seconds']):
                    f['seconds'](s)
        elif(data[0]=='$'):
            s=''.join(data)
            if(f['message']):
                f['message'](s)
        elif(data[0]=='a'): #adc
            self.parse_adc(data)            
            if(f['adc']):
                f['adc'](self.adc)
            for f in f['osf']:
                f()
            self.f['osf']=[]
    def connect(self):
        self.com.connect()
    def disconnect(self):
        self.com.disconnect()
    def destroy(self):
        try:
            self.network.kill()
            self.com.disconnect()
        except:
            pass
    def request_id(self):
        d=self.d
        #print self.com.is_open()
        #if self.com.is_open():
        self.com.write(d['request_id'])
class Kit:  #Name wrapper class
    def __init__(self):
        self.__kit__=Armadillo()
        k=self.__kit__
        self.connect=k.connect
        self.destroy=k.destroy
        self.disconnect=k.disconnect
        self.d=k.d # data
        self.f=k.f # functions
        self.register=k.network.register
        self.network=k.network
if __name__=="__main__":
    kit=Kit()    
    kit.connect()
    kit.register()
    kit.network.sh.serve_forever() 
    #kit.network.write("text")

#!/usr/bin/env python
__copyright__ = 'Copyright (C) 2010 Mustafa Sakarya'
__author__    = 'Mustafa Sakarya mustafasakarya1986@gmail.com'
__license__   = 'GNU GPLv3 http://www.gnu.org/licenses/'
try:
    import serial
except:
    print("Please install PySerial")
    print("http://pyserial.sourceforge.net/index.html")
import time
import threading
from collections import deque
import socket
import cPickle

class TTimer(threading.Thread):
    def __init__(self, func,interval=1):
        threading.Thread.__init__(self)       
        self.func=func
        self.interval=interval
        self.enabled=False
        self.cnt=0
    def run(self):
        while 1:
            if self.enabled:
                self.func(self)
            if time:
                time.sleep(self.interval)
    def kill(self):
        self.enabled=False
        self._Thread__stop()
        
class COM:
    def __init__(self,read_cbf=None):
        self.serial=serial.Serial(timeout=0)
        self.port="/dev/ttyUSB0"
        self.baudrate=57600        
        self.read_cbf=read_cbf
        self.preamble=['A','U']
        self.rxbuff=deque()
        self.timer=TTimer(self.t1f,0.5)
        self.timer.start()        
    def connect(self):
        print("Connecting to "+self.port)
        ser=self.serial
        self.serial.port=self.port
        self.serial.baudrate=self.baudrate        
        try:
            self.serial.open()            
        except:
            print("Can't open serial port")        
        if ser.isOpen():            
            self.timer.enabled=True
            #ser.setRTS(0)
            #ser.setDTR(0)
        self.rxstep=0
        self.rxcnt=0
        self.nsum=0
        self.rxsize=0
    def disconnect(self):
        print("Closing "+self.port)
        if self.serial.isOpen():
            self.serial.close()
        self.timer.enabled=False
    def t1f(self,kendi):   #poll rx data
        rxbuff=self.rxbuff
        rxdata=self.serial.readline()
        for d in rxdata:
            rxbuff.appendleft(d)
        length=len(rxbuff)
        if length>4:  #enough data available?
            self.depack()
    def depack(self):        
        rxbuff=self.rxbuff
        step=self.rxstep
        cnt=self.rxcnt
        nsum=self.nsum
        size=self.rxsize
        pr=self.preamble
        while((step<3 and len(rxbuff)>0) or(step==3 and len(rxbuff)>size)):
            if(step==0):
                temp=rxbuff.pop()
                if(temp==pr[0]):
                    step=step+1                
            elif (step==1):
                temp=rxbuff.pop()
                if(temp==pr[1]):
                    step=step+1
                else:
                    step=0                
            elif (step==2):
                temp=ord(rxbuff.pop())
                size=temp -ord('A') #*********
                if(size<64):
                    step=step+1
                else:
                    step=0
                cnt=0                
            elif (step==3):
                if(size==cnt):                    
                    temp=ord(rxbuff[-size-1])                    
                    if(temp==(255-nsum)):
                        tempbuff=[]
                        for i in range(size):
                            tempbuff.append(rxbuff.pop())
                        self.read_cbf(tempbuff)                    
                    step=0
                    nsum=0
                    cnt=0                    
                else:
                    try:
                        nsum = (nsum+ord(rxbuff[-cnt-1]))%256
                        cnt=cnt+1       
                    except:
                        step=0
                        nsum=0
                        cnt=0
    def write(self,data):
        if(isinstance(data,str)):
            l=[]                
            for d in data:
                l.append(ord(d))
            data=l[:]
        txpack=self.pack(data[:])       
        if self.serial.isOpen():
            self.serial.write(str(bytearray(txpack)))            
        else:
            for d in txpack:
                self.rxbuff.appendleft(d)
            print(txpack)
            self.depack()        
    def pack(self,data=None):
        size=[len(data)+ord('A')]  #******
        sum=0
        for d in data:
            sum=(sum+d)%256
        sum=[255-sum]
        txpack=self.preamble[:]+size[:]+data[:]+sum[:]
        return txpack[:]    
    def destroy(self):
        self.timer.kill()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
class TClient:
    def __init__(self,prc='sub',ip="localhost"):        
        host = ip
        if prc=='sub':
            port=21568
        else: #'main'
            port=21567
        port = port
        buf = 1024
        self.addr = (host,port)
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    def send(self,data):
        msg=cPickle.dumps(data)
        self.UDPSock.sendto(msg,self.addr)        
class TServer(threading.Thread):
    def __init__(self,prc='main',rcbf=None,ip="localhost",port=None):
        threading.Thread.__init__(self)  
        self.rcbf=rcbf        
        host = ip
        if not port:            
            if prc=='sub':
                port=21567
            else: #'main'
                port=21568
        port = port
        self.buf = 1024
        #addr = ("192.168.1.43",43180)#("85.101.34.130",43180)
        addr = ("localhost",43180)#(host,port)
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDPSock.bind(addr)
    def receive(self): 
        print "receive"   
        data,addr = self.UDPSock.recvfrom(self.buf)            
        try:
            msg= cPickle.loads(data)
        except:
            msg=data
        
        return msg
    
    def run(self):
        while 1:
            data=self.receive()
            self.rcbf(data)            
    def kill(self):        
        self._Thread__stop()
        
#s="/home/mustafa/elektronik/python/projects/dene.py"
#subprocess.call(["python", s])
def srcbf(data):
    print data,'from call back'
if __name__=="__main__":
    c=TClient("sub")
    #s=TServer("main",rcbf=srcbf)
    #s.start()
    l=[1,2,3]
    c.send(l)
    c.send("print 'selam'")
    time.sleep(0.1)
    #s.kill()    
    print("main")
    #com=COM()
